#!/usr/bin/env bash

make clean
make html

rm -rf mydoc

mkdir mydoc
cd mydoc
git clone -b gh-pages https://github.com/exleym/Flask-Filter.git
cd Flask-Filter
rm *

touch .nojekyll
cp -r ../../documentation/build/html/* .
git add .
git commit -m "sphinx documentation changes"
git push
