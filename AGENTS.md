# AGENTS.md - Master AI Engineering Playbook & Operating Directives

Welcome to **aru-golden-path-demo**. This repository operates under **Aru_Agentic_SDLC** governance.

Primary technology stack: **python**.

All AI agents operating within this repository MUST follow the directives, skills, and tools defined herein.

---

## 🚨 Core Governance: The Issue-First Law

**No code change, refactor, or feature implementation may begin without first originating from a tracked issue on the GitHub Project Board.**

---

## 🏭 Process Ownership and Merge Authority

**Aru_Agentic_SDLC owns this repository's issue-to-merge lifecycle.** Other
installed frameworks may assist within the current Aru step, but may not
replace the Project Board, independently claim work, create an ungoverned
branch, or merge around the Definition-of-Done gate.

- GSD lifecycle/resume hooks and `.planning/HANDOFF.json` are disabled or
  non-authoritative here.
- Brainstorming frameworks supply input to Aru's plan gate rather than running
  a parallel lifecycle.
- Memory tools provide context only. PR bots are reviewers, not merge
  authorities.

After a distinct agent completes the independent review and every enforced
gate passes, any factory agent, including the implementation author, may
execute the mechanical merge only through
`python3 "$ARU_SDLC_HOME/scripts/merge_pr.py" --pr <ID>`. Authors must never
self-review. Direct pushes and ad-hoc merge commands are forbidden. Money,
PII, security, schema, migration, irreversible behavior, large diffs, and
review-round count increase planning, testing, and review depth but do not
create a human gate. Human intervention is reserved for a severe merge
conflict or merge/close-out failure that agents cannot safely resolve through
governed remediation.

---

## 🎯 Primary Directives for AI Agents

1. **Execute via SkillsMP Skills** (in `$ARU_SDLC_HOME/skills/`):
   - Router: `aru-agentic-sdlc/SKILL.md`
   - Primary Skill: `implement-next-issue/SKILL.md`
   - Issue Creation: `create-github-issue/SKILL.md`
   - Code Review Skill: `code-review/SKILL.md`
   - CI Failure Remediation: `remediate-ci-failure/SKILL.md`
   - PR Review Feedback: `address-pr-feedback/SKILL.md`
2. **Worktree Isolation**:
   - Always run feature work inside `.worktrees/` directories to keep the main workspace clean.
3. **Local Test Verification First**:
   - Run `pytest -q` and confirm all tests pass before committing.
4. **Mandatory Issue Linking**:
   - Every Pull Request MUST include `Closes #<issue_number>` in its body.
5. **Cursor**: Prefer installed personal skills / slash commands from the
   machine-level Cursor integration (`docs/cursor-integration.md` in
   `$ARU_SDLC_HOME`). Do not vendor a second copy of SDLC skills into this repo.
6. **Plan Gate**: Before the first edit, `type:feat`, `needs-design`, money,
   PII, schema, migration, and other irreversible work posts the implementation
   plan required by `implement-next-issue`. High-risk scope triggers the gate
   regardless of issue type labels. The plan is always post-and-proceed unless
   the issue lacks a product decision needed to define acceptance; risk alone
   does not require human acknowledgement.

---

## 📋 Board Contract

Issue bodies drive the dependency engine. Every issue MUST carry:

```
depends-on: #12, #14        (omit or leave blank if none)
parallel-eligible: true     (only when it has no unresolved depends-on)
touches: src/**, tests/**    (all paths this issue may modify)
```

Board statuses, in order: `Backlog` → `Ready` → `In Progress` → `In Review` → `Done`.
Each is mirrored by a `status:*` label so the CLI and the board stay in sync.
