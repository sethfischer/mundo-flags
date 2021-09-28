#!/usr/bin/env bash

shopt -s globstar

exit_code=0

directory="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

while IFS= read -r -d $'\0' filename; do
    if [ -f "$filename" ]; then
        echo "Check formatting of ${filename}"
        diff "$filename" <(scour --quiet -i "$filename" \
            --nindent=2 \
            --indent=space \
            --keep-unreferenced-defs \
            --protect-ids-noninkscape \
            --disable-simplify-colors \
            --enable-comment-stripping \
            --strip-xml-space \
            --disable-style-to-xml) 1>&2
        # shellcheck disable=SC2181
        if [ $? -ne 0 ]; then
            exit_code=1
            echo "Fail"
        else
            echo "Pass"
        fi
    fi
done < <(git ls-files -z -- "${directory}/**.svg")

exit $exit_code
