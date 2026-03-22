import requests as r
from bs4 import BeautifulSoup as bs

ENTRY_URL = "http://soushu2030.com"  # 填入永久网址
next_url = ENTRY_URL

def get_new_url(next_url):
    while True:
        res = r.get(next_url)
        
        # 如果 text 中包含 "forum.php"，则停止循环
        if "forum.php" in res.text:
            return next_url
        
        # 解析页面内容，寻找跳转地址
        soup = bs(res.text, "html.parser")
        redirect_meta = soup.find("meta", attrs={"http-equiv": "refresh"})
        if redirect_meta is None:
            link = soup.find("a")
            if link is None:
                raise Exception("Unexpected page structure: no redirect meta tag and no link found.")
            else:
                return link.get("href")

        else:
            content = redirect_meta.get("content")
            if content is None:
                raise Exception("Unexpected meta tag structure: no content attribute found.")
            else:
                url_part = content.split(";")[1].strip()
                if not url_part.lower().startswith("url="):
                    raise Exception("Unexpected meta tag structure: content does not contain a URL.")
                next_url = url_part[4:].strip()
                if not next_url.startswith("http"):
                    next_url = ENTRY_URL + next_url

if __name__ == "__main__":
    final_url = get_new_url(next_url)
    print("搜书吧新url:", final_url)
    file_content = []
    with open("config.txt", "r", encoding="utf-8") as filer:
        file_content = filer.read().splitlines()
        print("已读取config.txt")
    file_content[0] = final_url
    with open("config.txt", "w", encoding="utf-8") as filew:
        filew.write("\n".join(file_content))
        print("已更新config.txt")