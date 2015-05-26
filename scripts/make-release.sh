#!/bin/sh

rm -rf tmp/pyccle-eebo-phase1
mkdir -p tmp/pyccle-eebo-phase1

cd tmp/pyccle-eebo-phase1
ln -s ../../metadata/dates-eebo.csv .
ln -s ../../README.md .
ln -s ../../LICENSE .

mkdir texts
cd texts
for i in $(cat ../../../misc/texts-phase1.txt); do
    ln -s ~/hdd/eebo-tagged/$i.tag .
done

cd ../..
tar -c -z -h -f pyccle-eebo.tgz pyccle-eebo-phase1/
