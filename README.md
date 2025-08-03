# git-author-sync

`git-author-sync` is a cross-platform tool to rewrite the author and committer identity of all Git commits using a new (typically corporate) identity.

It uses `git-filter-repo`, the modern and officially recommended alternative to `git filter-branch`.

---

## Purpose

This tool is intended for developers who:

- Worked on code using a personal Git identity
- Need to rewrite their commit history with corporate credentials
- Want an automated and safe way to sanitize Git metadata before pushing to a company repository

---

## Project Structure

```
git-author-sync/
├── config_user.txt        # Identity mapping file
├── git-filter-repo.py     # Official git-filter-repo script
├── rewrite_commits.py     # Python controller script
└── README.md              # This documentation
```

---

## Requirements

- Python 3.6 or higher
- Git installed and available in PATH
- `git-filter-repo.py` must be present in this directory (no installation required)

---

## Configuration (`config_user.txt`)

Edit the file `config_user.txt` with the identity mapping to be applied:

```
OLD_NAME=your-personal-name
OLD_EMAIL=your.personal@email.com
NEW_NAME=your-corporate-name
NEW_EMAIL=your.corporate@email.com
```

All fields are required. The `OLD_*` values must match exactly what appears in:

```bash
git log --pretty=format:"%an <%ae>" | sort | uniq
```

---

## How to Use

### 1. Run the script from inside your Git project folder, pointing to the tool path

You **do not need to copy `git-author-sync/` into your project**. Simply be inside the Git repo you want to rewrite and call the script directly.

#### On Windows:

```powershell
python C:\path\to\git-author-sync\rewrite_commits.py
```

#### On Linux/macOS:

```bash
python3 /path/to/git-author-sync/rewrite_commits.py
```

This will:

- Load `config_user.txt`
- Run `git-filter-repo` with the configured identity
- Rewrite all commits across all branches and tags
- Remove the remote origin (as a safety measure)

---

## After Rewriting: Push to a New Remote Repository

### If you're working on a personal machine for testing:

1. Create a new empty repository on GitHub (without README)
2. Add the new remote:

```bash
git remote add origin https://github.com/your-username/your-test-repo.git
```

3. Force-push the rewritten history:

```bash
git push --force --tags origin 'refs/heads/*'
```

---

## Real-World Use (Corporate Environment)

In a company setup:

- You typically **already have the destination repo created**
- After rewriting locally, you just need to:

```bash
git remote set-url origin https://github.com/company-org/your-repo.git
git push --force --tags origin 'refs/heads/*'
```

---

## Best Practices

- Always work on a backup or disposable copy of the repository
- Only push to remotes you control (never shared ones)
- Double check commit logs after rewriting with:

```bash
git log --all --graph --decorate
```

---

## Credits

Based on the official git-filter-repo tool:  
https://github.com/newren/git-filter-repo
