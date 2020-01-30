#!/bin/bash

set -eux

CSDN_ID="qq_38105251"
mail_host="smtp.163.com"
mail_port=465
mail_user="shenkebug@163.com"
mail_password="wuTAwuai10190013"
sender="shenkebug@163.com"
receiver="shenkebug@qq.com"
filePath="config.json"

if [ ! -f "$filePath" ];then
touch $filePath
echo "result = {
            "nick_name": "",
            "blog_title": "",
            "profile": {}
        }" > $filePath
echo "文件创建完成"
else
echo "文件已经存在"
fi

python spider.py $CSDN_ID $mail_host $mail_port $mail_user $mail_password $sender $receiver $filePath
