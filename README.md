# aru-golden-path-demo

A small public reference consumer for **Aru Code Factory**: a landing page,
product checks, and an issue-to-merge workflow on the
[project board](https://github.com/users/gillella/projects/6).

## Factory revision

The consumer governance files were reconciled with Factory commit
`ea0101b34353f451dcf2ced455894df965b5137a` on September 10, 2026.

```bash
export ARU_SDLC_HOME=/path/to/Aru_Agentic_SDLC
export ARU_SDLC_REF=ea0101b34353f451dcf2ced455894df965b5137a
```

Use a separate Factory checkout at that immutable revision. Setting these
variables does not check out the revision, update this repository's copied
files, install a shared Hermes adapter, or start agents. Follow the pinned
Factory [operations guide](https://github.com/gillella/Aru_Agentic_SDLC/blob/ea0101b34353f451dcf2ced455894df965b5137a/docs/OPERATIONS.md)
when installing or reconciling an existing consumer.

Factory lifecycle helpers and skills remain under `$ARU_SDLC_HOME`; this
repository owns its application, tests, and deployment workflows.

## Build and check the page

From this repository's root, using Python 3.12:

```bash
bash .aru/verify-project.sh
python3 scripts/build_preview.py
test -f dist/index.html
```

The build copies the public site into `dist/` and rejects unsafe source or output
paths. Open `dist/index.html` to inspect it locally. The product tests exercise
build containment and HTML acceptance. The governed PR workflow also runs
`.aru/verify.sh` on this repository's assigned `self-hosted-mac` runner.

## Development workflow

1. Shape an issue with acceptance criteria, dependencies, and a `touches:` scope.
2. Claim Ready work and implement it in an isolated worktree.
3. Open a PR linked to the issue and pass current-head verification.
4. Resolve findings and obtain a distinct authoritative review when required by risk.
5. Merge through the pinned Factory helper with `--pr <number>` and
   `--expected-head <40-character-PR-head>`. Confirm merge and board close-out.
6. Deploy through this consumer's release process, with a selected artifact,
   operator approval, health checks, and a retained rollback artifact.

The optional external Hermes Driver schedules bounded development actions.
Enabling it does not deploy this application.

## Deployment status and remaining work

The existing `Deploy Preview` workflow targets GitHub Pages. Source and CI
success do not establish that a site is deployed. Before relying on the demo as
a deployment reference, configure the Pages target and approval boundary, bind
the served files to an immutable artifact, and demonstrate deployment, health
verification, and restoration of a previously deployed artifact.

The `Record Governed Promotion` workflow is an audit-only record; its successful
status is not proof of deployment. Factory's
[deployment guidance](https://github.com/gillella/Aru_Agentic_SDLC/blob/ea0101b34353f451dcf2ced455894df965b5137a/integrations/deployment/README.md)
defines the evidence the consumer must produce. Deployment and rollback remain
unproven until an operator records successful live runs.
