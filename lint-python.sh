#!/usr/bin/env bash

set -o errexit -o noclobber -o nounset

directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

git ls-files -z -- "${directory}/**.py" | xargs --no-run-if-empty --null black --check
git ls-files -z -- "${directory}/**.py" | xargs --no-run-if-empty --null flake8
git ls-files -z -- "${directory}/**.py" | xargs --no-run-if-empty --null isort --profile black --check-only
git ls-files -z -- "${directory}/**.py" ':!:tests/*' | xargs --no-run-if-empty --null pydocstyle --convention=pep257
