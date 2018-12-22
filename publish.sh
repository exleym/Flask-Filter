#!/bin/bash


set -e # exit with nonzero exit code if anything fails


#if [[ $TRAVIS_BRANCH == "master" && $TRAVIS_PULL_REQUEST == "false" ]]; then
if [[ 1 == 1 ]]; then
echo "Starting to update gh-pages\n"

# Make static docs with Sphinx-Build and copy it to clean mydoc/
make clean
make html
rm -rf mydoc
mkdir mydoc

# Clone gh-pages branch and copy static docs into new repo
cd mydoc
git clone -b gh-pages https://github.com/exleym/Flask-Filter.git
cd Flask-Filter
rm -r *
touch .nojekyll
cp -r ../../documentation/build/html/* .

# Commit changes back to GitHub
git commit -a -m "sphinx documentation changes"
git push

echo "Done updating gh-pages\n"

else
 echo "Skipped updating gh-pages, because build is not triggered from the master branch."
fi;