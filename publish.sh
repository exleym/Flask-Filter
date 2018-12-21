#!/usr/bin/env bash

make clean
make html

rm -rf mydoc

mkdir mydoc
cd mydoc
git clone -b gh-pages https://github.com/exleym/Flask-Filter.git

cp ../documentation/build/html/* .
git commit -am "sphinx documentation changes"
git push
