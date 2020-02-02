#!/bin/bash

set -eux

# 修改为你的 CSDN_ID
CSDN_ID="sculpta"

# 每次访问文章的间隔，单位:分钟
interval=20

python csdn-spider/spider.py $CSDN_ID $interval