import sys
import requests
from bs4 import BeautifulSoup
import time
import numpy as np


# 访问网页
def access_page(url):
    user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
        "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; GTB7.0)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; ) AppleWebKit/534.12 (KHTML, like Gecko) Maxthon/3.0 Safari/534.12",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E; SE 2.X MetaSr 1.0)",
        "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.33 Safari/534.3 SE 2.X MetaSr 1.0",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E) QQBrowser/6.9.11079.201",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)",
        "Mozilla/5.0 (BlackBerry; U; BlackBerry 9800; en) AppleWebKit/534.1+ (KHTML, like Gecko) Version/6.0.0.337 Mobile Safari/534.1+",
        "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.0; U; en-US) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/233.70 Safari/534.6 TouchPad/1.0",
        "Mozilla/5.0 (SymbianOS/9.4; Series60/5.0 NokiaN97-1/20.0.019; Profile/MIDP-2.1 Configuration/CLDC-1.1) AppleWebKit/525 (KHTML, like Gecko) BrowserNG/7.1.18124",
        "Openwave/ UCWEB7.0.2.37/28/999",
        "NOKIA5700/ UCWEB7.0.2.37/28/999",
        "UCWEB7.0.2.37/28/999",
        "Mozilla/4.0 (compatible; MSIE 6.0; ) Opera/UCWEB7.0.2.37/28/999"
    ]

    user_agent = np.random.choice(user_agent_list, 1)[0]
    headers = {"user-agent": user_agent}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return None


# 爬取访问量、排名等信息
# flag: 是否需要爬取该页面下的文章，默认:需要
def access_article(text, flag=True):
    soup = BeautifulSoup(text, "html.parser")

    if (flag):
        # 爬取每条文章的信息
        articles = soup.find_all(["strong", "h4"])
        if (articles == []):
            return 0
        else:
            # 随机爬取文章
            length = len(articles)
            index_array = np.random.permutation(np.arange(length))
            for index in index_array:
                article = articles[index]
                article_title = article.a.get_text().strip()
                article_url = article.a.get("href")
                print(article_title, article_url)

                # 随机生成一个间隔时间（范围：15~25分钟）
                interval = np.random.randint(15 * 60, 25 * 60, 1)
                access_page(article_url)
                time.sleep(interval)

            return 1
    else:
        # 爬取asideProfile信息
        nick_name = soup.find("a", id="uid").get("title")
        read = soup.find_all("dl", attrs={"class": "text-center"})[-1].get("title")
        return nick_name, read


# 保存email内容
def saveEmail(email_path, message):
    with open(email_path, 'w', encoding="utf-8") as email:
        email.writelines(message)


if __name__ == "__main__":

    CSDN_ID = sys.argv[1]

    # CSDN_ID = "sculpta"

    email_path = "email.txt"
    page_num = 1
    url_prefix = "https://blog.csdn.net/" + CSDN_ID + "/article/list/"

    url = url_prefix + str(page_num)

    try:
        while (1):
            print("第" + str(page_num) + "页：")
            if (access_article(access_page(url))):
                page_num += 1
                url = url_prefix + str(page_num)
            else:
                print("目前在第" + str(page_num) + "页，该页没有内容，结束")
                break

        # 任务完成后，获取访问量
        url = url_prefix + str(1)
        nick_name, read = access_article(access_page(url), flag=False)
        call = "亲爱的 " + nick_name + "，您的csdn spider完成任务啦\n"
        message = call + "目前博客的访问量是：" + str(read)

        saveEmail(email_path, message)

    except TypeError:
        print("返回的状态码不是200")
    except Exception as e:
        print(e)
