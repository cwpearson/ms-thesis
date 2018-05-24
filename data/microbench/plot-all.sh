#! env bash

set -eou pipefail -x

for y in *.yml; do
    pdf="${y%%.*}.pdf";
    yml=$y;
    if [ $yml -nt $pdf ]; then
        nice -n20 ./plot.py "${y%%.*}.pdf" "$y" &
    fi
done
wait

for y in *.yml; do
    pdf="${y%%.*}.pdf";
    yml=$y;
    if [ $yml -nt $pdf ]; then
        nice -n20 ./plot.py "${y%%.*}.pdf" "$y"
    fi
done