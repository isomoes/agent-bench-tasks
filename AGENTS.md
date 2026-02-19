# AGENTS.md — Agent Bench Tasks

This repository contains benchmark task definitions (YAML) and verification scripts (Python).

```
tasks/
├── tools/          # Task YAML files (e.g. find-os-001.yaml)
├── verify/         # Verification scripts (e.g. find-os-001.py)
└── results/        # Output directory written by agents during task execution
```

---

## Task YAML Format

Place task files in `tools/<task-id>.yaml`. The `id` field must match the filename stem.

```yaml
id: CATEGORY-NNN              # Unique task ID (e.g. TOOLS-001, BUG-042)
title: "Short human-readable title"
category: tools               # bug-fix | feature | refactor | tools
difficulty: easy              # easy | medium | hard

source:
  repository: https://github.com/org/repo.git
  commit: "main"              # branch name or full commit SHA

prompt: |
  Detailed instructions for the agent.
  Multi-line. Markdown is fine.

verification:
  type: python                # python | pytest | bash
  command: "python3 verify/CATEGORY-NNN.py"
  timeout: 30                 # seconds (default: 60)

permissions:
  mode: "dontAsk"             # dontAsk | bypassPermissions | default
  write: true                 # Allow Write/Edit tools
  bash: true                  # Allow Bash tool
  read: true                  # Allow Read/Glob/Grep tools
  web_fetch: false            # Allow WebFetch/WebSearch tools

metadata:
  tags:
    - python
    - system-info
```

### Field Reference

| Field | Required | Values |
|-------|----------|--------|
| `id` | yes | `CATEGORY-NNN` — uppercase, matches filename |
| `category` | yes | `bug-fix`, `feature`, `refactor`, `tools` |
| `difficulty` | yes | `easy`, `medium`, `hard` |
| `source.commit` | yes | branch name or full SHA |
| `verification.timeout` | no | seconds, default `60` |
| `permissions.mode` | no | `dontAsk` auto-approves all prompts |
| `max_iterations` | no | positive integer, caps agent loop |

---

## Verification Script Conventions

Place scripts in `verify/<task-id>.py`. The script runs with the task workspace as the
working directory, so all paths are relative to the workspace root.

### Rules

- Shebang: `#!/usr/bin/env python3`
- Print `PASS: <description>` on success, `FAIL: <reason>` on failure
- Exit `0` on pass, `1` on fail
- Read agent output from `results/<filename>` (relative to workspace root)
- Standard library only — no third-party dependencies

### Template

```python
#!/usr/bin/env python3
"""Verification script for <task-id>."""
import os
import sys


def verify() -> bool:
    output_file = "results/output.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()

    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    # Add task-specific validation here
    print(f"PASS: {content}")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
```

### Validation Tips

- Always check file existence before reading
- Strip whitespace before comparing strings (`content.strip()`)
- Use `.lower()` for case-insensitive keyword checks
- Provide specific failure messages that explain what was wrong and what was expected
- Avoid hardcoding platform-specific values; use `platform` or `os` to detect the environment

### Example — OS version check

```python
#!/usr/bin/env python3
"""Verify OS version was written correctly."""
import os
import sys
import platform


def verify() -> bool:
    output_file = "results/os_version.txt"

    if not os.path.exists(output_file):
        print(f"FAIL: '{output_file}' does not exist")
        return False

    content = open(output_file).read().strip()
    if not content:
        print(f"FAIL: '{output_file}' is empty")
        return False

    os_keywords = ["linux", "macos", "darwin", "windows"]
    if not any(kw in content.lower() for kw in os_keywords):
        print(f"FAIL: '{content}' does not look like an OS version string")
        return False

    print(f"PASS: OS version correctly detected: {content}")
    return True


if __name__ == "__main__":
    sys.exit(0 if verify() else 1)
```

---

## Running a Verification Script Directly

```bash
python3 verify/find-os-001.py
```

Scripts exit `0` on PASS and `1` on FAIL.
