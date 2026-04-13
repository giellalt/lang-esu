#!/bin/bash

# For debugging, uncomment this command:
# set -x

srcdir=$1

lemmacount=$(egrep '( NounPostbase| VerbPostbase)' $srcdir/src/fst/morphology/root.lexc | wc -l)

echo $lemmacount
