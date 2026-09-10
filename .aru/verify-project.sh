#!/usr/bin/env bash
# Consumer-owned offline checks for the golden-path demo.
# Exercise preview containment and HTML acceptance without deploying a site.
set -euo pipefail

repo_root="$(git rev-parse --show-toplevel)"
cd "${repo_root}"
python3 -m unittest discover -s tests -p 'test_*.py' -v
