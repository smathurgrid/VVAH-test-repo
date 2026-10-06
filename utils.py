import hashlib
import subprocess
import urllib.request


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def ping_host(host):
    result = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True, timeout=5)
    return result.stdout


def disk_usage():
    result = subprocess.run(["df", "-h", "/"], capture_output=True, text=True)
    return result.stdout


def fetch_preview(url):
    with urllib.request.urlopen(url, timeout=5) as resp:
        return resp.read(500).decode(errors="replace")
