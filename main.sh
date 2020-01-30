#!/bin/bash

set -eux

CSDN_ID="qq_38105251"
# mail_host="smtp.163.com"
# mail_port=465
# mail_user="shenkebug@163.com"
# mail_password="wuTAwuai10190013"
# sender="shenkebug@163.com"
# receiver="shenkebug@qq.com"
filePath="result.txt"
emailPath="email.txt"

touch $emailPath

python spider.py $CSDN_ID $filePath $emailPath

ll -h