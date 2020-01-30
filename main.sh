#!/bin/bash

set -eux

CSDN_ID="qq_38105251"
filePath="result/result.txt"
emailPath="result/email.txt"

touch $emailPath

python spider.py $CSDN_ID $filePath $emailPath