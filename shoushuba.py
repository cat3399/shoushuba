# -*- coding:utf-8 -*-
import re
import time
import os
import requests
from lxml import etree
import random

pl_session=requests.session()

def login(user_name, user_password,base_url):
    session = requests.session()
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.76"
    logging_api = f"{base_url}/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1 "  # 登录接口
    headers = {
        "Cache-Control": "no-cache",
        "Content-Type": "application/x-www-form-urlencoded",
        "Pragma": "no-cache",
        "Referer": base_url,
        "User-Agent": user_agent
    }
    # 表单参数
    data = {
        'username': user_name,
        'password': user_password,
        'quickforward': "yes",
        'handlekey': "ls"}
    # 登录账号
    res = session.post(url=logging_api, headers=headers, data=data).text
    if f"window.location.href='{base_url}';" in res:
        print(f'账号：{user_name} 登录成功！！！')
    else:
        print('出现错误，请重试！！！')
    # 获取银币数量
    user_info_url = f"{base_url}/home.php?mod=spacecp&ac=credit&showcredit=1"
    user_info_response = session.get(url=user_info_url, headers=headers, verify=True)
    if user_info_response.status_code == 200:
        print("用户信息页面获取成功:")
    else:
        print("用户信息页面获取失败")
    html_content = user_info_response.text
    html_tree = etree.HTML(html_content)
    user_info_xpath = '//*[@id="ct"]/div[1]/div/ul[2]/li[1]/text()'
    formhash=html_tree.xpath("//input[@name='formhash']/@value")[0]
    # print(formhash)
    user_info_elements = html_tree.xpath(user_info_xpath)
    if '\xa0' in user_info_elements[0]:
        yinbi=user_info_elements[0].strip('\xa0').strip('')
        print('银币数量获取成功')
        print('当前银币数量:',yinbi)
        return [session,headers,formhash,base_url]
    else:
        print("银币数量获取失败")
    time.sleep(3)

    # pl(session,headers)

def get_yinbi(session,headers,formhash,base_url):
    user_info_url = f"{base_url}/home.php?mod=spacecp&ac=credit&showcredit=1"
    user_info_response = session.get(url=user_info_url, headers=headers, verify=True)
    # if user_info_response.status_code == 200:
    #     print("用户信息页面获取成功:")
    # else:
    #     print("用户信息页面获取失败")
    html_content = user_info_response.text
    html_tree = etree.HTML(html_content)
    user_info_xpath = '//*[@id="ct"]/div[1]/div/ul[2]/li[1]/text()'
    user_info_elements = html_tree.xpath(user_info_xpath)
    if '\xa0' in user_info_elements[0]:
        yinbi = user_info_elements[0].strip('\xa0').strip('')
        print('银币数量获取成功')
        print('当前银币数量:', yinbi)
        return [session, headers, formhash, base_url]
    else:
        print("银币数量获取失败")
    time.sleep(3)


def pl(session,headers,formhash,base_url,i,url_list):
    message=['别的不说，楼主就是给力啊','谢谢楼主分享，祝搜书吧越办越好！','看了LZ的帖子，我只想说一句很好很强大！','太感谢了太感谢了太感谢了']
    commen=random.choice(message)

    comment_payload = {
        'formhash': formhash,
        'handlekey': 'register',
        'noticeauthor': '',
        'noticetrimstr': '',
        'noticeauthormsg': '',
        'usesig': '1',
        'subject': '',
        'message': commen
    }
    tid=random.choice(url_list)
    pl_url=base_url+f'/forum.php?mod=post&infloat=yes&action=reply&fid=100&extra=&tid={tid}&replysubmit=yes&inajax=1'
    pinglun=session.post(url=pl_url,headers=headers,data=comment_payload)
    # print(pinglun.text)
    if '发布成功' in pinglun.text :
        i+=1
        get_yinbi(session, headers, formhash, base_url)
        print(f'评论成功，此次评论的帖子tid为 {tid} ,评论的内容为 {commen} ,等待60s后再次评论')

        return i
    elif '回复限制' in pinglun.text:
        print('重复评论')
    elif '发布间隔' in pinglun.text:
        print('评论太快，等待60s')

    else:
        print('评论失败')
        print(f'错误代码：{pinglun.status_code}')
        time.sleep(1)
    return i

def get_url(session,headers,base_url):
    url=f'{base_url}/forum.php?mod=forumdisplay&fid=39&page=1'
    # print(url)
    page_text=session.get(url=url,headers=headers).text
    page_root=etree.HTML(page_text)
    page_need=page_root.xpath("//table[@id='threadlisttableid']")
    pattern = re.compile('tid=(\d+)&amp')
    page_need_text=str(etree.tostring(page_need[0]))
    tid_list = pattern.findall(page_need_text)
    tid_list_set = list(dict.fromkeys(tid_list))[10::]
    return tid_list_set

if __name__ == '__main__':
    # user_name=input("输入账户名称")
    user_name=''
    # user_password=input("输入账户密码")
    user_password=''
    base_url=''
    text=''
    if os.path.exists('config.txt')==False:
        with open('config.txt', 'a+', encoding='UTF-8') as fp:
            simple_text = base_url+ '\n' + 'username' + '\n' + 'userpassword'
            fp_text = fp.write(simple_text)

    with open('config.txt','a+',encoding='UTF-8') as fp:
        fp.seek(0)
        fp_text = fp.readlines()
        user_name=fp_text[1].strip('\n').strip('')
        user_password=fp_text[2].strip('\n').strip('')
        base_url=fp_text[0].strip('\n').strip('')
    while True:
        try:
            if user_name=='username':
                print(f'请替换当前目录下config.txt中的username与password为你的账号密码，并且在第一行填入搜书吧的url，例如 https://www.284djs.soushu2028.com/ ,如果搜书吧域名更改，请更改为新的域名')
                break
            else :
                info=login(user_name,user_password,base_url)
                # print(info)
                break
        except Exception as ex:
            time.sleep(3)
            print('失败')
            print(ex)
    url_list=get_url(info[0], info[1], base_url)
    num=0
    while num<=7:
        i=pl(info[0],info[1],info[2],info[3],num,url_list)
        if i <=2:
            # print(i)
            num=i

        else:
            print('成功评论三次')
            break
        time.sleep(65)
    time.sleep(5)
