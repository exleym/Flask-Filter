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
#using token clone gh-pages branch
git clone --quiet --branch=gh-pages https://${GH_TOKEN}@github.com/${GH_USER}/${GH_REPO}.git gh-pages > /dev/null
echo "cloned gh-pages branch from ${GH_REPO}"
echo "Directory looks like:"
ls -al
cd gh-pages
echo "Clearing directory and adding new documentation"
rm -r *
touch .nojekyll
cp -r ../../documentation/build/html/* .

# Commit changes back to GitHub
echo "Beginning publishing stage ..."
git add .
git commit -m "sphinx documentation changes"
git push

echo "Done updating gh-pages\n"

else
 echo "Skipped updating gh-pages, because build is not triggered from the master branch."
fi;