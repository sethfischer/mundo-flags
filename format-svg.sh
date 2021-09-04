#! /bin/bash

set -e

for filename in svg/*.svg; do
    scour -i "$filename" -o "$filename"scoured \
        --disable-simplify-colors \
        --disable-style-to-xml \
        --indent=space \
        --keep-unreferenced-defs \
        --nindent=2 \
        --protect-ids-noninkscape \
        --strip-xml-space
    mv -- "$filename"scoured "$filename"
done
