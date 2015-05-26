#!/bin/sh

rm -rf tmp/pyccle-ecco
mkdir -p tmp/pyccle-ecco

cd tmp/pyccle-ecco
ln -s ../../metadata/dates-ecco.csv .
ln -s ../../README.md .
ln -s ../../LICENSE .

mkdir texts
cd texts

ln -s ~/hdd/ecco-tagged/*.tag .

cd ../..
tar -c -z -h -f pyccle-ecco.tgz pyccle-ecco/
