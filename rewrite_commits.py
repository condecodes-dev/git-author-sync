import os
import subprocess
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "config_user.txt")
FILTER_REPO = os.path.join(SCRIPT_DIR, "git-filter-repo.py")

if not os.path.exists(CONFIG_PATH):
    print(f"[ERROR] config_user.txt not found in {SCRIPT_DIR}")
    sys.exit(1)

if not os.path.exists(FILTER_REPO):
    print(f"[ERROR] git-filter-repo.py not found in {SCRIPT_DIR}")
    sys.exit(1)

config = {}
with open(CONFIG_PATH, "r") as f:
    for line in f:
        if "=" in line and not line.strip().startswith("#"):
            key, value = line.strip().split("=", 1)
            config[key] = value

required = ["OLD_NAME", "OLD_EMAIL", "NEW_NAME", "NEW_EMAIL"]
missing = [k for k in required if k not in config]
if missing:
    print(f"[ERROR] Missing fields in config_user.txt: {', '.join(missing)}")
    sys.exit(1)

name_cb = f"""
if name == b"{config['OLD_NAME']}": return b"{config['NEW_NAME']}"
return name
"""

email_cb = f"""
if email == b"{config['OLD_EMAIL']}": return b"{config['NEW_EMAIL']}"
return email
"""

print("[INFO] Rewriting commit history using git-filter-repo...\n")

cmd = [
    sys.executable,
    FILTER_REPO,
    "--force",
    "--name-callback", name_cb,
    "--email-callback", email_cb,
]

try:
    subprocess.run(cmd, check=True)
except subprocess.CalledProcessError:
    print("[ERROR] git-filter-repo failed.")
    sys.exit(1)

try:
    branch = subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"]).decode().strip()
    origin = subprocess.check_output(["git", "remote", "get-url", "origin"]).decode().strip()
    print(f"\n✅ History rewritten successfully.")
    print(f"\n🟡 Current branch: {branch}")
    print(f"🔗 Remote origin: {origin}")
    print(f"\n👉 To push your changes:\n  git push --force --tags origin 'refs/heads/*'")
except:
    print("\n✅ History rewritten. No remote origin detected.")
