# actions-bot——several robots based on GitHub Actions 🤖

目前包含两个 email 机器人，都是基于 GitHub Actions 实现的

- weather-emailbot：参照阮一峰老师的一篇教程：[GitHub Actions 教程：定时发送天气邮件](http://www.ruanyifeng.com/blog/2019/12/github_actions.html)

- csdn-emailbot：爬取 CSDN profile 信息，在 runner 服务器部署爬虫环境，并定时发送邮件，可参考 [我的博客](https://blog.csdn.net/qq_38105251/article/details/104119623)

## 使用方法 ʕ •ᴥ•ʔ

### 1. 首先点击右上角 🌟Star , 🔱Fork（推荐）或 clone

`git clone https://github.com/profoundly/actions-bot.git`

### 2. 修改

  - 对于 weather-emailbot，需修改 `weather.sh` 中的城市信息（具体可参考 [chubin/wttr.in](https://github.com/chubin/wttr.in)）以及将 `weather.yml` 中 Send mail 步骤的 `to` 字段修改你要接收邮件的邮箱地址
  
  - 对于 csdn-emailbot，需修改 `main.sh` 中的 `CSDN_ID` 为你的 CSDN_ID，以及将 `weather.yml` 中 Send mail 步骤的 `to` 字段修改你要接收邮件的邮箱地址，另外还可以自定义更多玩法，可参考 [我的博客](https://blog.csdn.net/qq_38105251/article/details/104119623)

### 3. 配置 SMTP 邮件发送服务

以网易邮箱为例，选择「设置」中的 「POP3/SMTP/IMAP」，打上勾✔之后保存，然后设置密码

**注意**：该密码不能跟邮箱密码一致

然后，将 SMTP 的用户名和密码添加到仓库的「Secrets」中，如下图所示：

<p align="center">
    <img src="https://gitee.com/profoundly/data/raw/master/blog/github-actions-spider/img.png" width="80%">
</p>

其中，`MAIL_USERNAME` 是你开通 SMTP 服务的邮箱，`MAIL_PASSWORD` 是你设置的 SMTP 服务的密码（**不是邮箱的登录密码**）

### 4. 创建 Workflow

进入仓库的「Actions」，点击「New workflow」、「Set up a workflow yourself」，然后复制 `.github/workflows/` 文件夹下的 `yml` 文件代码，粘贴并 commit，完成 👌

### 5. enjoy it