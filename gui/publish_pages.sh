#!/usr/bin/env bash
# Copies the generated Gazette (gui/site) into docs/ for GitHub Pages.
cd "$(dirname "$0")/.." && rm -rf docs && mkdir docs && cp -r gui/site/. docs/ && touch docs/.nojekyll
