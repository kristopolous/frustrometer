#!/bin/bash

set -x
# The plugin js is the same that is used for the site.
cp ../site/js/frustrometer.js chrome/
cp ../site/js/frustrometer.js gecko/
