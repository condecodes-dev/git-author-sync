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

git-author-sync/
├── config_user.txt # Identity mapping file
├── git-filter-repo.py # Official git-filter-repo script
├── rewrite_commits.py # Cross-platform Python controller
└── README.md # This documentation

---

## Requirements

- Python 3.6 or higher
- Git installed and available in PATH
- `git-filter-repo.py` must be present in this directory (no installation required)

---

## Configuration (`config_user.txt`)

Edit the file `config_user.txt` to reflect your identity mapping:

```
OLD_NAME=your-personal-name
OLD_EMAIL=your.personal@email.com
NEW_NAME=your-corporate-name
NEW_EMAIL=your.corporate@email.com
```

All four fields are required. The `OLD_*` values must match exactly what appears in:

```bash
git log --pretty=format:"%an <%ae>" | sort | uniq
```

---

## How to Use

Place the git-author-sync/ folder next to your Git project folder.

Example structure:

```
/Documents/
├── my-project/
└── git-author-sync/
```

From inside your Git project (e.g. my-project), run:

```bash
python ../git-author-sync/rewrite_commits.py
```

The script will:

- Load the identity mapping from config_user.txt
- Run git-filter-repo with force
- Rewrite all commits across all branches and tags
- Output push instructions

---

## Example Output

```
[INFO] Rewriting commit history using git-filter-repo...

History rewritten successfully.

Current branch: main
Remote origin: https://github.com/your-org/your-repo.git

To push your changes, run:
  git push --force --tags origin 'refs/heads/*'
```

---

## Notes and Best Practices

- Always make a backup of your repository before rewriting
- Do not run this on shared branches or after collaborators have pulled
- Use git push --force responsibly

---

## Credits

Based on the official git-filter-repo tool:  
https://github.com/newren/git-filter-repo
