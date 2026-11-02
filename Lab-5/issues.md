# Lab 5: Static Code Analysis — Issue Table

**Name:** Aryan Musale  
**SRN:** PES1UG24CS085  
**Section:** CSE-B  
**File analysed:** `address_book.py` (Contact & Address Book Manager)

Line numbers refer to the original `address_book.py`. Baseline reports are in `reports/before/`, post-fix reports in `reports/after/`.

## Baseline results

| Tool   | Before fixes |
|--------|--------------|
| Pylint | 5.47/10 (29 messages) |
| Bandit | 4 issues: 1 High, 1 Medium, 2 Low |
| Flake8 | 4 issues |

## Identified issues (high and medium severity first)

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Weak MD5 hash | Bandit B324 | Security | High | 19 | `hashlib.md5()` is a broken hash; Bandit flags it because it could be mistaken for a security use. Here it only builds a short display ID. | Pass `usedforsecurity=False` so the intent is explicit. This keeps the same 6-character IDs (e.g. `ecc177`), so the output does not change. |
| 2 | Unsafe pickle deserialisation | Bandit B301 | Security | Medium | 67 | `pickle.load()` can execute arbitrary code if `contacts.bak` is tampered with. | Back up and restore with `json.dump()` / `json.load()`. The data is plain strings in dicts, so JSON holds it fully and safely. |
| 3 | pickle module imported | Bandit B403 | Security | Low | 3 | Importing `pickle` is flagged as a deserialisation risk. | Remove the import; replace with `json`. |
| 4 | Hardcoded password | Bandit B105 | Security | Low | 6 | `SYNC_PASSWORD = "contacts-demo"` puts a secret in source code (and in git history). | Read it from the `CONTACTS_SYNC_PASSWORD` environment variable instead of hardcoding it. |
| 5 | Overly broad exception | Pylint W0718 | Bug | Medium | 34 | `except Exception` hides unrelated bugs (e.g. a typo) behind the "No contact named" message. | Catch only `KeyError`, the error raised for a missing contact. |
| 6 | open() without encoding | Pylint W1514 | Bug | Medium | 54 | The CSV file's encoding depends on the OS locale, so names with non-ASCII characters can break across machines. | Add `encoding="utf-8"` to `open()`. |
| 7 | Non-snake_case names | Pylint C0103 | Style / Convention | Low | 10, 18, 22, 30, 39, 47, 53, 60, 65 | camelCase function and argument names (`addContact`, `fullName`, `fileName`, …) break PEP 8 naming. | Rename to snake_case (`add_contact`, `full_name`, `file_name`, …) and update every call in `main()`. |
| 8 | Missing docstrings | Pylint C0114 / C0116 | Documentation | Low | 1, 10, 18, 22, 30, 39, 47, 53, 60, 65, 70 | No module docstring and no function docstrings. | Add a module docstring and a one-line docstring to every function. |
| 9 | range(len()) loop | Pylint C0200 | Code quality | Low | 49 | Indexing with `range(len(names))` is less readable than iterating directly. | Use `enumerate(sorted(contacts), start=1)`. |
| 10 | Script runs on import | Code review (good practice) | Design | Low | 88 | `main()` runs at import time, so importing the module triggers file writes. | Wrap the call in an `if __name__ == "__main__":` guard. |
| 11 | Missing whitespace around operator | Flake8 E225 | Style | Low | 23 | `found=[]` | `found = []` |
| 12 | Too many blank lines | Flake8 E303 | Style | Low | 47 | Three blank lines before `printDirectory`. | Reduce to the PEP 8 standard of two. |
| 13 | Missing whitespace after comma | Flake8 E231 | Style | Low | 84 | `"| first:",sorted(...)` | Add a space after the comma. |
| 14 | Line too long | Flake8 E501 | Style | Low | 85 | 86 characters, over the 79-character limit. | Split the `print()` arguments across lines. |

## Commits

1. Baseline: original code, before reports, this issue table
2. Bandit fixes: issues 1–4
3. Pylint fixes: issues 5–10
4. Flake8 fixes: issues 11–14
5. After reports and verification

## Verification

| Tool   | Before | After |
|--------|--------|-------|
| Pylint | 5.47/10 | **10.00/10** |
| Bandit | 4 issues (1 High, 1 Medium, 2 Low) | **No issues identified** |
| Flake8 | 4 issues | **0 issues** (`reports/after/flake8_report.txt` is empty because Flake8 prints nothing when the code is clean) |

The program prints the same output before and after the fixes. The demo still adds 3 valid contacts, rejects the invalid phone number, reports the missing contact, generates `ecc177` for Neha, and restores a backup that matches the in-memory book.
