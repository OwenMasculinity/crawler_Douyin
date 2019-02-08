from splinter.driver.webdriver.chrome import Options, Chrome
from splinter.browser import Browser
from contextlib import closing
import requests, json, time, re, os, sys, time
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
chrome_path = "C:\Program Files (x86)\Google\Chrome\chromedriver.exe"

headers = {
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'zh-CN,zh;q=0.9',
			'cache-control': 'max-age=0',
			'upgrade-insecure-requests': '1',
			'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
		}
class DouYin(object):
    def __init__(self, width=500, height=300):
        """
        抖音App视频下载
        """
        # 无头浏览器
        chrome_options = Options()
        chrome_options.add_argument(
            'user-agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"')
        self.driver = Browser(driver_name='chrome', executable_path=chrome_path, options=chrome_options,
                              headless=True)

    def get_video_urls(self, user_id):
        """
        获得视频播放地址
        Parameters:
            user_id：查询的用户ID
        Returns:
            video_names: 视频名字列表
            video_urls: 视频链接列表
            nickname: 用户昵称
        """
        video_names = []
        video_urls = []
        unique_id = ''
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Linux; U; Android 5.1.1; zh-cn; MI 4S Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.146 Mobile Safari/537.36 XiaoMi/MiuiBrowser/9.1.3',
        }
        # 991734700
        # 8527081
        # 108561773
        while unique_id != user_id:
            search_url = 'https://api.amemv.com/aweme/v1/discover/search/?cursor=0&keyword=%s&count=10&type=1&retry_type=no_retry&iid=17900846586&device_id=34692364855&ac=wifi&channel=xiaomi&aid=1128&app_name=aweme&version_code=162&version_name=1.6.2&device_platform=android&ssmix=a&device_type=MI+5&device_brand=Xiaomi&os_api=24&os_version=7.0&uuid=861945034132187&openudid=dc451556fc0eeadb&manifest_version_code=162&resolution=1080*1920&dpi=480&update_version_code=1622' % user_id
            req = requests.get(url=search_url, verify=False,headers=headers)
            html = json.loads(req.text)
            # print("获取到的html",html)
            aweme_count = html['user_list'][0]['user_info']['aweme_count']
            uid = html['user_list'][0]['user_info']['uid']
            nickname = html['user_list'][0]['user_info']['nickname']
            unique_id = html['user_list'][0]['user_info']['unique_id']
            print(aweme_count)
            print(uid)
            print(nickname)
            print(unique_id)
        # user_url = "https://api.amemv.com/aweme/v1/aweme/post/?user_id={}&max_cursor=0&count={}".format(uid, aweme_count)
        # user_url = 'https://www.douyin.com/aweme/v1/aweme/post/?user_id=%s&max_cursor=0&count=%s' % (uid, aweme_count)
        #     user_url = "https://api.amemv.com/aweme/v1/aweme/post/?user_id={}&max_cursor=0&count={}".format(uid,aweme_count)
            user_url = 'https://www.amemv.com/aweme/v1/aweme/post/?user_id=%s&max_cursor=0&count=%s' % (uid, aweme_count)
            # headers = {"Accept-Encoding": "gzip","Cache-Control": "max-stale=60","Host": "api.amemv.com","Connection": "Keep-Alive","Cookie": "odin_tt=d51e5e7ffda1f563bc1fe73c97e33e04f01bfc12789fb9639ae2bc15718bf427598bd8572179ab4e5e98923309e31530; sid_guard=d3cb3e34bd94f9f06343e2df4344acaf%7C1527501273%7C2592000%7CWed%2C+27-Jun-2018+09%3A54%3A33+GMT; uid_tt=5c91b3d10e4f90d2958eac7a77541f26; sid_tt=d3cb3e34bd94f9f06343e2df4344acaf; sessionid=d3cb3e34bd94f9f06343e2df4344acaf; qh[360]=1","User-Agent": "okhttp/3.7.0.6"}
            req = requests.get(url=user_url,verify=False, headers=headers).content.decode()
            # print("用户主页",req)
            html = json.loads(req)
            i = 1
            for each in html['aweme_list']:
                share_desc = each['share_info']['share_desc']
                # print("share_desc",share_desc)
                if '抖音-原创音乐短视频社区' == share_desc:
                    video_names.append(str(i) + '.mp4')
                    i += 1
                else:
                    video_names.append(share_desc + '.mp4')
                video_urls.append(each['share_info']['share_url'])

        return video_names, video_urls, nickname

    def get_download_url(self,video_url, watermark_flag):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        req = requests.get(video_url, verify=False, headers=headers).text
        # s = 'class="video-player" src="https://aweme.snssdk.com/aweme/v1/playwm/?video_id=v0200f9a0000bc5tb7vqabaf947o54hg&amp;line=0"'
        download_url = re.findall(r'class="video-player" src="(.*?)"', req)[0]
        print(download_url)
        return download_url

    def video_downloader(self,video_urls, video_names, watermark_flag=False):
        for i in range(len(video_urls)):
            try:
                video_url = video_urls[i]
                video_name = video_names[i]
                size = 0
                video_url = self.get_download_url(video_url, watermark_flag=watermark_flag)
                with closing(requests.get(video_url, headers=headers, verify=False, stream=True)) as response:
                    chunk_size = 1024
                    content_size = int(response.headers['content-length'])
                    if response.status_code == 200:
                        sys.stdout.write('  [文件大小]:%0.2f MB\n' % (content_size / chunk_size / 1024))
                    video_name = "抖音视频下载"+video_name
                    with open(video_name, "wb") as file:
                        for data in response.iter_content():
                            file.write(data)
                            size += len(data)
                            file.flush()

                            sys.stdout.write('  [下载进度]:%.2f%%' % float(size / content_size * 100) + '\r')
            except Exception as e:
                print(e)

    def run(self):
        user_id = input('请输入ID(例如108561773):')
        video_names, video_urls, nickname = self.get_video_urls(user_id)
        print(video_urls)
        print(video_names)
        self.video_downloader(video_urls, video_names, watermark_flag=False)

if __name__ == '__main__':
    douyin = DouYin()
    douyin.run()