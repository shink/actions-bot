#!/bin/python
#Coding="utf-8"

import sys
import requests
from bs4 import BeautifulSoup
import json
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# 爬取访问量、排名等信息
def getResult(CSDN_ID):
    url = "https://blog.csdn.net/" + CSDN_ID
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-language": "zh-CN,zh;q=0.9"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        result = {
            "nick_name": "",
            "blog_title": "",
            "profile": {}
        }

        soup = BeautifulSoup(response.text, "html.parser")

        # 爬取asideProfile信息
        nick_name = soup.find("a", id="uid").get("title")
        blog_title = soup.find("a", attrs={"href": url}).get_text().strip()
        result["nick_name"] = nick_name
        result["blog_title"] = blog_title

        profile = {}
        profile_data = []
        data_info = soup.find("div", attrs={"class": "data-info d-flex item-tiling"})
        data = data_info.find_all("dl", attrs={"class": "text-center"})
        for num in data:
            profile_data.append(num.attrs["title"])

        grade_info = soup.find("div", attrs={"class": "grade-box clearfix"}).contents
        point = grade_info[5].find("dd").attrs["title"]
        week_rank = grade_info[3].attrs["title"]
        total_rank = grade_info[7].attrs["title"]

        profile["original"] = profile_data[0]
        profile["fans"] = profile_data[1]
        profile["like"] = profile_data[2]
        profile["comment"] = profile_data[3]
        profile["read"] = profile_data[4]
        profile["point"] = point
        profile["week_rank"] = week_rank
        profile["total_rank"] = total_rank
        result["profile"] = profile

        return result


# 生成信息
def formatMessage(result):
    message = ""
    call = "亲爱的 " + result["nick_name"] + "，您的 CSDN 信息到啦\n\n"
    profile = result["profile"]
    original = "原创文章数目： " + profile["original"] + "\n"
    fans = "粉丝： " + profile["fans"] + "\n"
    like = "获赞： " + profile["like"] + "\n"
    comment = "评论： " + profile["comment"] + "\n"
    read = "访问量： " + profile["read"] + "\n"
    point = "积分： " + profile["point"] + "\n"
    week_rank = "周排名： " + profile["week_rank"] + "\n"
    total_rank = "总排名： " + profile["total_rank"]

    message += call + original + fans + like + comment + read + point + week_rank + total_rank
    return message


# 发送邮件
def sendEmail(content):
    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = "GitHub Actions<" + sender + ">"
    message['To'] = "<" + receiver + ">"

    subject = "CSDN Report"
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)
        smtpObj.login(mail_user, mail_password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


# 保存email内容
def saveEmail(email_path, message):
    with open(email_path, 'w', encoding="utf-8") as email:
        email.writelines(message)


if __name__ == "__main__":

    CSDN_ID = sys.argv[1]

    res = getResult(CSDN_ID)
    message = formatMessage(res)
    email_path = "email.txt"
    saveEmail(email_path, message)
