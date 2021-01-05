# Several robots based on GitHub Actions 🤖

<p align="center">
    <img src="https://img.shields.io/github/license/shink/actions-bot.svg"/>
    <img src="https://img.shields.io/github/repo-size/shink/actions-bot.svg"/>
    <img src="https://img.shields.io/github/last-commit/shink/actions-bot.svg"/>
    <img src="https://img.shields.io/badge/language-python-blue.svg">
</p>

目前包含两个 email 机器人，都是基于 GitHub Actions 实现的

- weather-emailbot：定时发送天气邮件，参照了阮一峰老师的一篇教程：[GitHub Actions 教程：定时发送天气邮件](http://www.ruanyifeng.com/blog/2019/12/github_actions.html)

- csdn-emailbot：爬取 CSDN profile 信息，在 runner 服务器部署爬虫环境，并定时发送邮件，可参考 [我的博客](https://blog.csdn.net/sculpta/article/details/104142607)

## 使用方法 ʕ •ᴥ•ʔ

### 1. 首先点击右上角 🌟Star , 🔱Fork（推荐）或 Clone

```git
git clone https://github.com/shink/actions-bot.git
```

> **注意：** 向 master 分支 push 时才会触发 Actions。Fork 本仓库后 clone 到本地，随便修改一点内容并 push 到 master 分支，即可触发

### 2. 修改

  - 对于 weather-emailbot，需修改 `main.sh` 中的城市信息（具体可参考 [chubin/wttr.in](https://github.com/chubin/wttr.in)）以及将 `weather.yml` 中 Send mail 步骤的 `to` 字段修改你要接收邮件的邮箱地址
  
  - 对于 csdn-emailbot，需修改 `main.sh` 中的 `CSDN_ID` 为你的 CSDN_ID，以及将 `csdn-emailbot.yml` 中 Send mail 步骤的 `to` 字段修改你要接收邮件的邮箱地址，另外还可以自定义更多玩法，可参考 [我的博客](https://blog.csdn.net/sculpta/article/details/104142607)

### 3. 配置 SMTP 邮件发送服务

以网易邮箱为例，选择「设置」中的 「POP3/SMTP/IMAP」，打上勾 ✔ 之后保存，然后设置密码

**注意**：该密码不能跟邮箱密码一致

然后，将 SMTP 的用户名和密码添加到仓库的「Secrets」中，如下图所示：

<p align="center">
    <img src="https://gitee.com/tsund/data/raw/master/blog/2020/01/github-actions-spider/img.png" width="800">
</p>

其中，`MAIL_USERNAME` 是你开通 SMTP 服务的邮箱，`MAIL_PASSWORD` 是你设置的 SMTP 服务的密码（**不是邮箱的登录密码**）

### 4. 创建 Workflow

进入仓库的「Actions」，点击「New workflow」、「Set up a workflow yourself」，然后复制 `.github/workflows/` 文件夹下的 `yml` 文件代码，粘贴并 commit，完成 👌

### 5. Just Enjoy It

## License

[Apache License 2.0](LICENSE)
