#!/usr/bin/env python3
"""check_touches.py - Fail-closed enforcement of PR file modifications against issue declared touches:"""

import fnmatch
import json
import os
import re
import subprocess
import sys


def run_cmd(cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return res.returncode, res.stdout.strip(), res.stderr.strip()


def parse_touches(body):
    if not body:
        return []
    match = re.search(
        r"^[ \t]*[*_`]{0,2}touches[*_`]{0,2}[ \t]*:[ \t]*([^\n]*)",
        body,
        re.IGNORECASE | re.MULTILINE,
    )
    if not match:
        return []
    raw = match.group(1).strip().strip("*_").strip()
    if raw.startswith("("):
        return []
    return [p.strip().strip("`") for p in raw.split(",") if p.strip()]


def norm_path(p):
    return p.strip().strip("/")


def path_allowed(rel_path, touches):
    if not rel_path or not touches:
        return False
    rel = norm_path(rel_path)
    for pat in touches:
        pat_norm = norm_path(pat)
        if pat_norm == "**":
            return True
        if rel == pat_norm:
            return True
        if "*" in pat_norm or "?" in pat_norm or "[" in pat_norm:
            pattern_regex = re.escape(pat_norm)
            pattern_regex = pattern_regex.replace(r"\*", r"[^/]*")
            pattern_regex = pattern_regex.replace(r"\?", r"[^/]")
            if re.fullmatch(pattern_regex, rel):
                return True
        else:
            bp = pat_norm.rstrip("/")
            if bp and (rel.startswith(bp + "/") or rel == bp):
                return True
    return False


def main():
    pr_body = os.environ.get("PR_BODY", "")
    pr_head = os.environ.get("PR_HEAD", "")

    # Parse all linked Closes #N issues from body and branch name
    issue_nums = set(re.findall(r"\bcloses\s+#(\d+)\b", pr_body, re.IGNORECASE))
    if pr_head:
        m_head = re.search(r"issue-(\d+)", pr_head, re.IGNORECASE)
        if m_head:
            issue_nums.add(m_head.group(1))

    if not issue_nums:
        print("::error:: Fail-closed: No linked issue (Closes #N) found in PR body or branch name; cannot verify touches budget.", file=sys.stderr)
        sys.exit(1)

    combined_touches = []
    for num in sorted(issue_nums):
        code, out, err = run_cmd(["gh", "issue", "view", num, "--json", "body", "-q", ".body"])
        if code != 0 or not out:
            print(f"::error:: Fail-closed: Could not fetch issue #{num} body: {err}", file=sys.stderr)
            sys.exit(1)

        touches = parse_touches(out)
        if not touches:
            print(f"::error:: Fail-closed: Issue #{num} declares no touches: metadata line.", file=sys.stderr)
            sys.exit(1)
        combined_touches.extend(touches)

    code, changed, err = run_cmd(["git", "diff", "--name-only", "origin/main...HEAD"])
    if code != 0:
        print(f"::error:: Fail-closed: Could not execute git diff query: {err}", file=sys.stderr)
        sys.exit(1)

    changed_files = [f.strip() for f in changed.splitlines() if f.strip()]
    if not changed_files:
        print("✅ No changed files detected in PR diff.")
        sys.exit(0)

    violations = [f for f in changed_files if not path_allowed(f, combined_touches)]

    if violations:
        print(f"::error:: PR modifies files outside declared touches: {', '.join(combined_touches)}", file=sys.stderr)
        for v in violations:
            print(f"::error:: Violation: {v}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ All {len(changed_files)} changed files are within declared touches budget ({', '.join(combined_touches)}).")


if __name__ == "__main__":
    main()
