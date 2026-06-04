1. 

```shell
apt install ffmpeg

curl -LsSf https://astral.sh/uv/install.sh | sh
export UV_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
source $HOME/.local/bin/env 

uv venv
uv pip install requests openai requests_toolbelt
```

2. pipeline.py 
```py
import argparse
import os
import sys
import io
import time
import hashlib
import threading
import subprocess
import json
import requests
from datetime import datetime
from openai import OpenAI

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# ── Config ──────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TMP_DIR = "/tmp/video_pipeline" if sys.platform != "win32" else os.path.join("D:\\","video_pipeline")
SIZE_THRESHOLD_MB = 450
OVERLAP_SEC = 30
MODEL_EP = None
client = None

# ── Helpers ─────────────────────────────────────────────
def load_config():
    global MODEL_EP, client
    conf = {}
    with open(os.path.join(SCRIPT_DIR, "env.conf"), "r") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line:
                k, v = line.split("=", 1)
                conf[k] = v
    MODEL_EP = conf["EP"]
    client = OpenAI(
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        api_key=conf["KEY"],
    )


def human_size(n):
    if n < 1024:
        return "%d B" % n
    elif n < 1024 * 1024:
        return "%.1f KB" % (n / 1024)
    else:
        return "%.1f MB" % (n / 1024 / 1024)


def status(msg):
    print("[*] %s" % msg)


def fatal(msg):
    print("\n[!] %s" % msg)
    sys.exit(1)


# ── Step 1: Download ────────────────────────────────────
def download_video(url, out_path, threads=4):
    head = requests.head(url, allow_redirects=True, timeout=30)
    total = int(head.headers.get("Content-Length", 0))
    if total == 0:
        fatal("Cannot determine file size from server")

    accept_ranges = head.headers.get("Accept-Ranges", "") == "bytes"

    if not accept_ranges or total < 10 * 1024 * 1024:
        _download_sequential(url, out_path, total)
    else:
        _download_parallel(url, out_path, total, threads)


def _download_sequential(url, out_path, total):
    status("Downloading %s (single thread)" % human_size(total))
    downloaded = 0
    bar_width = 40
    start = time.time()
    resp = requests.get(url, stream=True, timeout=600)
    resp.raise_for_status()

    with open(out_path, "wb") as f:
        for chunk in resp.iter_content(8192):
            f.write(chunk)
            downloaded += len(chunk)
            _show_bar(downloaded, total, start, bar_width)
    print()
    elapsed = time.time() - start
    print("[*] Done in %.1fs (%.1f MB/s)" % (elapsed, total / elapsed / 1024 / 1024))


def _download_parallel(url, out_path, total, num_threads):
    status("Downloading %s (%d threads)" % (human_size(total), num_threads))

    chunk_size = (total + num_threads - 1) // num_threads
    downloaded = [0] * num_threads
    lock = threading.Lock()
    start = time.time()
    bar_width = 40
    errors = []

    # Pre-allocate file
    with open(out_path, "wb") as f:
        f.truncate(total)

    def _worker(tid, byte_start, byte_end):
        headers = {"Range": "bytes=%d-%d" % (byte_start, byte_end)}
        try:
            resp = requests.get(url, headers=headers, stream=True, timeout=600)
            resp.raise_for_status()
            with open(out_path, "r+b") as f:
                f.seek(byte_start)
                pos = byte_start
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
                    pos += len(chunk)
                    downloaded[tid] = pos - byte_start
                    with lock:
                        _show_bar(sum(downloaded), total, start, bar_width)
        except Exception as e:
            errors.append(e)

    ranges = []
    for i in range(num_threads):
        s = i * chunk_size
        e = min(s + chunk_size, total) - 1
        if s < total:
            ranges.append((s, e))

    threads_list = []
    for tid, (s, e) in enumerate(ranges):
        t = threading.Thread(target=_worker, args=(tid, s, e))
        threads_list.append(t)
        t.start()

    for t in threads_list:
        t.join()

    if errors:
        fatal("Download failed: %s" % errors[0])

    print()
    elapsed = time.time() - start
    print("[*] Done in %.1fs (%.1f MB/s)" % (elapsed, total / elapsed / 1024 / 1024))


def _show_bar(downloaded, total, start, bar_width=40):
    pct = downloaded / total
    elapsed = time.time() - start
    speed = downloaded / elapsed if elapsed > 0 else 0
    eta = (total - downloaded) / speed if speed > 0 else 0
    filled = int(bar_width * pct)
    bar = "[" + "=" * filled + " " * (bar_width - filled) + "]"
    sys.stdout.write(
        "\r  %s %5.1f%%  %s/s  ETA %ds  " % (
            bar, pct * 100, human_size(speed), int(eta)
        )
    )
    sys.stdout.flush()


# ── Step 2: Probe ───────────────────────────────────────
def probe_video(path):
    result = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", path],
        capture_output=True, text=True, timeout=60, check=True,
    )
    info = json.loads(result.stdout)["format"]
    duration = float(info["duration"])
    bitrate = int(info.get("bit_rate", 0))
    if bitrate == 0 and duration > 0:
        bitrate = int(os.path.getsize(path) * 8 / duration)
    print("[*] Duration: %.0fs  |  Bitrate: %d kbps  |  Size: %s" % (
        duration, bitrate // 1000, human_size(int(info["size"]))
    ))
    return duration, bitrate


# ── Step 3: Plan splits ─────────────────────────────────
def plan_splits(duration, bitrate):
    chunk_bytes = SIZE_THRESHOLD_MB * 1024 * 1024
    chunk_sec = chunk_bytes * 8 / bitrate if bitrate > 0 else 600
    chunk_sec = max(chunk_sec, 60)
    chunks = []
    start = 0.0
    while start < duration:
        end = min(start + chunk_sec, duration)
        chunks.append((start, end))
        if end >= duration:
            break
        start = end - OVERLAP_SEC
    print("[*] %d chunks (~%.0fs each, %ds overlap):" % (len(chunks), chunk_sec, OVERLAP_SEC))
    for i, (s, e) in enumerate(chunks):
        print("    Chunk %d: %.0fs - %.0fs (%.0fs)" % (i + 1, s, e, e - s))
    return chunks


# ── Step 4: Split ───────────────────────────────────────
OUTPUT_FORMAT = "%s.chunk_%02d.mp4"

def split_video(src_path, video_name, chunks):
    name_hash = hashlib.md5(video_name.encode()).hexdigest()[:8]
    paths = []
    for i, (ss, to) in enumerate(chunks):
        out = os.path.join(TMP_DIR, OUTPUT_FORMAT % (name_hash, i + 1))
        dur = to - ss
        if os.path.exists(out):
            print("[*] Chunk %d: %s (already exists)" % (i + 1, out))
            paths.append(out)
            continue
        print("[*] Splitting chunk %d/%d (%.0fs-%.0fs)..." % (i + 1, len(chunks), ss, to))
        subprocess.run([
            "ffmpeg", "-y", "-v", "error", "-stats",
            "-ss", str(ss), "-i", src_path,
            "-t", str(dur),
            "-c", "copy", "-movflags", "+faststart",
            out,
        ], check=True, timeout=600)
        size = os.path.getsize(out)
        print("    -> %s (%s)" % (out, human_size(size)))
        paths.append(out)
    return paths


# ── Step 5: Upload ──────────────────────────────────────
def upload_file(file_path, idx, total):
    file_size = os.path.getsize(file_path)
    label = "chunk %d/%d" % (idx, total)
    status("Uploading %s (%s)..." % (label, human_size(file_size)))

    bar_w = 30

    class UploadCB:
        def __init__(self):
            self.start = time.time()

        def __call__(self, monitor):
            pct = monitor.bytes_read / file_size
            elapsed = time.time() - self.start
            speed = monitor.bytes_read / elapsed if elapsed > 0 else 0
            eta = (file_size - monitor.bytes_read) / speed if speed > 0 else 0
            filled = int(bar_w * pct)
            bar = "[" + "=" * filled + " " * (bar_w - filled) + "]"
            sys.stdout.write(
                "\r    %s %5.1f%%  %s/s  ETA %ds  " % (
                    bar, pct * 100, human_size(speed), int(eta)
                )
            )
            sys.stdout.flush()

    with open(file_path, "rb") as f:
        encoder = MultipartEncoder(
            fields={
                "purpose": "user_data",
                "file": (os.path.basename(file_path), f, "video/mp4"),
                "preprocess_configs[video][fps]": "0.3",
            }
        )
        cb = UploadCB()
        monitor = MultipartEncoderMonitor(encoder, cb)
        r = requests.post(
            "https://ark.cn-beijing.volces.com/api/v3/files",
            headers={
                "Authorization": "Bearer " + client.api_key,
                "Content-Type": monitor.content_type,
            },
            data=monitor,
            timeout=600,
        )
    print()
    if r.status_code != 200:
        fatal("Upload failed: %s" % r.text)
    info = r.json()
    file_id = info["id"]
    print("    -> File ID: %s" % file_id)

    # Wait for preprocessing
    status("Waiting for preprocessing...")
    t0 = time.time()
    bar_frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    fi = 0
    while True:
        r = requests.get(
            "https://ark.cn-beijing.volces.com/api/v3/files/" + file_id,
            headers={"Authorization": "Bearer " + client.api_key},
        )
        info = r.json()
        if info.get("status") != "processing":
            break
        elapsed = int(time.time() - t0)
        sys.stdout.write(
            "\r    %s waiting... %ds elapsed   " % (bar_frames[fi % len(bar_frames)], elapsed)
        )
        sys.stdout.flush()
        fi += 1
        time.sleep(1)
    elapsed = int(time.time() - t0)
    st = info.get("status", "?")
    if st != "active":
        fatal("Preprocessing failed: %s" % info.get("error", info))
    print("\r    ✓ Ready! (%ds)                           " % elapsed)
    return file_id


# ── Step 6: Transcribe (streaming) ──────────────────────
def transcribe(file_id, idx, total):
    label = "chunk %d/%d" % (idx, total)
    print()
    status("Transcribing %s..." % label)

    stream = client.responses.create(
        model=MODEL_EP,
        input=[{
            "role": "user",
            "content": [
                {"type": "input_video", "file_id": file_id},
                {"type": "input_text", "text": "请将这段课程视频中的语音内容完整转写成文字，用中文输出，不要遗漏任何内容。"},
            ],
        }],
        stream=True,
    )

    text_parts = []
    event_count = 0
    has_output = False

    for event in stream:
        event_count += 1
        t = event.type
        if t == "response.reasoning_summary_text.delta":
            sys.stdout.write("\r\033[K    ◎%-5d" % event_count)
            sys.stdout.flush()
        elif t == "response.output_text.delta":
            text_parts.append(event.delta)
            clean = event.delta.replace("\n", "  ").replace("\r", "")
            if not has_output:
                print()
                has_output = True
            sys.stdout.write("\r\033[K    ↓%-5d " % event_count)
            sys.stdout.write(clean)
            sys.stdout.write("\033[K")
            sys.stdout.flush()
        elif t == "response.completed":
            u = event.response.usage
            print("\n    ✓ Done. events=%d  tokens(in=%d out=%d total=%d)" % (
                event_count, u.input_tokens, u.output_tokens, u.total_tokens
            ))
        else:
            sys.stdout.write("\r    ·%-5d" % event_count)
            sys.stdout.flush()

    return "".join(text_parts)


# ── Main ────────────────────────────────────────────────
def main():
    global SIZE_THRESHOLD_MB, OVERLAP_SEC, TMP_DIR
    load_config()

    parser = argparse.ArgumentParser(description="Video download + split + transcribe pipeline")
    parser.add_argument("url", nargs="?", help="Video URL")
    parser.add_argument("--chunk-size", type=int, default=SIZE_THRESHOLD_MB,
                        help="Max chunk size in MB (default: %d)" % SIZE_THRESHOLD_MB)
    parser.add_argument("--overlap", type=int, default=OVERLAP_SEC,
                        help="Overlap in seconds (default: %d)" % OVERLAP_SEC)
    parser.add_argument("--tmp-dir", default=TMP_DIR, help="Temp directory (default: %s)" % TMP_DIR)
    args = parser.parse_args()

    SIZE_THRESHOLD_MB = args.chunk_size
    OVERLAP_SEC = args.overlap
    TMP_DIR = args.tmp_dir

    url = args.url or input("Video URL: ").strip()
    if not url:
        fatal("No URL provided")

    os.makedirs(TMP_DIR, exist_ok=True)

    print("=" * 60)
    print("  Video -> Chunks -> Transcribe pipeline")
    print("  Chunk: %d MB | Overlap: %ds | Tmp: %s" % (SIZE_THRESHOLD_MB, OVERLAP_SEC, TMP_DIR))
    print("=" * 60)

    # 1. Download
    video_name = os.path.basename(url).split("?")[0] or "video.mp4"
    if not video_name.endswith(".mp4"):
        video_name += ".mp4"
    video_path = os.path.join(TMP_DIR, video_name)
    if not os.path.exists(video_path):
        download_video(url, video_path)
    else:
        print("[*] Video already downloaded: %s" % video_path)

    # 2. Probe
    duration, bitrate = probe_video(video_path)

    # 3. Plan
    chunks = plan_splits(duration, bitrate)

    # 4. Split
    chunk_paths = split_video(video_path, video_name, chunks)

    # 5 & 6. Upload + Transcribe each, save incrementally
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = os.path.join(".", "%s.txt" % timestamp)

    for i, chunk_path in enumerate(chunk_paths):
        try:
            file_id = upload_file(chunk_path, i + 1, len(chunk_paths))
        except Exception as e:
            fatal("Upload chunk %d failed: %s" % (i + 1, e))

        try:
            text = transcribe(file_id, i + 1, len(chunk_paths))
        except Exception as e:
            fatal("Transcription chunk %d failed: %s" % (i + 1, e))

        # Incremental save
        with open(output_path, "a", encoding="utf-8") as f:
            if i > 0:
                f.write("\n\n")
            f.write(text)

        print("    \033[32m✓ Saved to %s (%d chars)\033[0m" % (output_path, len(text)))

    # Cleanup
    for p in chunk_paths:
        try:
            os.remove(p)
        except:
            pass

    print()
    print("=" * 60)
    print("  All done! Output: %s" % output_path)
    print("=" * 60)


if __name__ == "__main__":
    from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
    main()
```