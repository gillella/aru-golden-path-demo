## Summary

Create this PR with `$ARU_SDLC_HOME/scripts/create_pr.py --issue N`.
The helper adds `Closes #N` automatically; omit closing directives from the
body supplied to the helper.

## Governed verification

The required `aru-governed-pr` server check runs this repository's
`.aru/verify.sh` on the exact PR head and validates the linked issue's
`touches:` declaration against the actual diff.

Optional local preflight or audit evidence:

- <!-- command and result, if useful -->

## Net surface change

Production LOC; test LOC; active docs; commands; skills; state stores:
