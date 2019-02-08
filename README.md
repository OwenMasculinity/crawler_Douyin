# 爬取少量视频（python+chrome）

- 将视频连接通过手机手动分享给电脑端
- 电脑端访问该视频连接，可通过python requests 库或chrome 浏览器手动下载

相关连接：

https://blog.csdn.net/LInthunder/article/details/82929564

https://www.jianshu.com/p/5f7dc1ed906e

# 爬取大量视频（python+Fiddler+appium）

- **Python**：利用requests 或者scrapy 库访问视频URL 并保存视频到本地文件夹中
- **Fiddler**：PC 端抓取手机抖音APP 包（需要手机与电脑在同一网段），获取视频URL，并将
URL 保存在TXT 文件中（注意：由于这里所获取的视频URL 是临时URL，有效时间为1 小
时，因此若要实现爬虫自动化，需要对“抖音”APP 不断刷新）
- **appium**：PC 端通过远程控制手机，无限刷新抖音app

相关连接：

https://www.cnblogs.com/stevenshushu/p/9635097.html

https://blog.csdn.net/weixin_41666747/article/details/80501923
