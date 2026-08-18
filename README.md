# aru-golden-path-demo

Public one-page product used to walk Aru_Agentic_SDLC from idea to preview.

The factory is **not** in this repository. `AGENTS.md` points at `$ARU_SDLC_HOME`.
Do not copy playbook `skills/` or lifecycle helpers (`claim_issue.py`, `merge_pr.py`,
and the rest) into this tree.

## Pin the playbook

S1.4 consumer pinning is `ARU_SDLC_REF`. This demo was written against playbook
commit `8d0513b` (2026-08-18 `origin/main`, includes the trust-boundary work).

```bash
export ARU_SDLC_HOME=/path/to/Aru_Agentic_SDLC
export ARU_SDLC_REF=8d0513b
"$ARU_SDLC_HOME/scripts/install_cursor_integration.sh"
```

Prefer an annotated `ckpt/<PR>-<sha7>` tag when you want the exact merge that
produced a checkpoint. Discover tags with `git -C "$ARU_SDLC_HOME" tag -l 'ckpt/*'`.
Do not pin the moving branch name `main` if you want a frozen walk.

## Runnable surface (before Pages)

```bash
python3 scripts/build_preview.py
# then open dist/index.html
# or open public/index.html directly
```

`scripts/build_preview.py` and `scripts/smoke_preview.py` are the consumer
preview pair written by `init_project.py` so GitHub Actions can assemble a
static artifact. They are not a second factory.

## Happy path

Board: [aru-golden-path-demo Board](https://github.com/users/gillella/projects/6)

1. File an idea (`$ARU_SDLC_HOME/skills/idea-to-prd/SKILL.md`). Seed idea: [#1](https://github.com/gillella/aru-golden-path-demo/issues/1).
2. Decompose an approved PRD (`prd-to-issues`). Seed implementation: [#2](https://github.com/gillella/aru-golden-path-demo/issues/2).
3. `python3 "$ARU_SDLC_HOME/scripts/fetch_next_work.py" --agent <id> --family <family> --claim`
4. Implement in `.worktrees/`. Open a PR with `create_pr.py` (`Closes #<n>`).
5. A **distinct** agent reviews. Authors never self-review.
6. `python3 "$ARU_SDLC_HOME/scripts/merge_pr.py" --pr <ID>`
7. `python3 "$ARU_SDLC_HOME/scripts/deploy_preview.py" --commit <40-char-sha> --issue <N>`

Every step leaves an issue or PR on this board. The first landing-page PR is
the seed walk; live Pages URL is recorded on the originating issue after a
peer review and gated merge.
