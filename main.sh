#!/bin/bash

set -eux

CSDN_ID="qq_38105251"
# mail_host="smtp.163.com"
# mail_port=465
# mail_user="shenkebug@163.com"
# mail_password="wuTAwuai10190013"
# sender="shenkebug@163.com"
# receiver="shenkebug@qq.com"
filePath="result/result.txt"
emailPath="result/email.txt"

if [ ! -f "$filePath" ];then
result='{
            "nick_name": "",
            "blog_title": "",
            "profile": {}
        }'
touch $filePath
echo $result > $filePath
echo "文件创建完成"
else
echo "文件已经存在"
result=""
cat $filePath | while read line
do
result=$result$line
done
fi

touch $emailPath

python spider.py $CSDN_ID $filePath $emailPath $result
