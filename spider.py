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
    # etree = lxml.html.etree

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

        # 爬取每条文章的信息
        # articles = []
        # article_list = soup.find("div", attrs={"class": "article-list"}).contents
        # for article in article_list:
        #     if (article != "\n"):
        #         articles.append(article)
        #
        # print(len(articles))
        #
        # for article in articles:
        #     string = article.find("a").get_text().strip()
        #     type = re.match(r'[\u4E00-\u9FA5]{2}', string).group()
        #     title = re.sub(r'^[\u4E00-\u9FA5]{2}', "（" + type + "）", string).replace(" ", "")
        #
        #     date = article.select(".date")[0].get_text().strip()
        #     info = article.select(".num")
        #     read_num = info[0].get_text().strip()
        #     comment_num = info[1].get_text().strip()
        return result


# 比对结果
def compare(before_res, res):
    message = ""
    if (before_res["nick_name"] == res["nick_name"] and before_res["blog_title"] == res["blog_title"]):
        call = "亲爱的 " + before_res["nick_name"] + "，"
        # 比较访问量、积分和排名
        if (before_res["profile"]["read"] != res["profile"]["read"]):
            before = int(before_res["profile"]["read"])
            after = int(res["profile"]["read"])
            message += call + "您的访问量增加了" + str(after - before) + "\n"

            if (before_res["profile"]["point"] != res["profile"]["point"]):
                before = int(before_res["profile"]["point"])
                after = int(res["profile"]["point"])
                message += call + "您的积分增加了" + str(after - before) + "分\n"

            if (before_res["profile"]["week_rank"] != res["profile"]["week_rank"]):
                before = int(before_res["profile"]["week_rank"])
                after = int(res["profile"]["week_rank"])
                message += call + "您的周排名上升了" + str(after - before) + "名\n"

        if (before_res["profile"]["total_rank"] != res["profile"]["total_rank"]):
            before = int(before_res["profile"]["total_rank"])
            after = int(res["profile"]["total_rank"])
            message += call + "您的总排名上升了" + str(after - before) + "名\n"

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


# 保存文件
def saveFile(res):
    json_str = json.dumps(res, indent=4, ensure_ascii=False)
    with open(file_path, 'w', encoding="utf-8") as json_file:
        json_file.write(json_str)


if __name__ == "__main__":

    CSDN_ID = sys.argv[1]
    mail_host = sys.argv[2]
    mail_port = sys.argv[3]
    mail_user = sys.argv[4]
    mail_password = sys.argv[5]
    sender = sys.argv[6]
    receiver = sys.argv[7]
    file_path = sys.argv[8]

    try:
        config_file = open(file_path, "r", encoding="utf-8")
        before_res = json.load(config_file)
        config_file.close()
        res = getResult(CSDN_ID)
        # 进行比对
        message = compare(before_res, res)
        print(message)
        if (message != ""):
            # 发送邮件
            sendEmail(message)
            saveFile(res)

    except FileNotFoundError:
        print("FileNotFound")
        res = getResult(CSDN_ID)
        saveFile(res)

    except Exception as e:
        res = getResult(CSDN_ID)
        saveFile(res)
