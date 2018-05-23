#! env bash

set -eou pipefail -x

for y in *.yml; do
    ./plot.py "${y%%.*}.pdf" "$y" &
done
wait