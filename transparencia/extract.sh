#!/bin/bash
libreoffice --invisible --convert-to html $1 --outdir /tmp/mpt/
mkdir /tmp/mpt/
sed  's/style=\"[^\"]*\"[^>]*//g' /tmp/mpt/$2  > /tmp/mpt/$2_nostyle.html
sed  's/align=\"[^\"]*\"[^>]*//g' /tmp/mpt/$2_nostyle.html  > /tmp/mpt/$2_noal.html
sed  's/height=\"[^\"]*\"[^>]*//g' /tmp/mpt/$2_noal.html  > /tmp/mpt/$2_nofont.html
sed  's/font=\"[^\"]*\"[^>]*//g' /tmp/mpt/$2_nofont.html  > /tmp/mpt/$2_nh.html
tidy --doctype html5  --word-2000 true --bare true  -q -utf8 -f /tmp/errs.txt  /tmp/mpt/$2_nh.html > /tmp/mpt/$2_clean.html
