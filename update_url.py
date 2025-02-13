import requests
from openai import OpenAI

# 从 config.txt 读取 old_url
with open("config.txt", "r", encoding="utf-8") as file:
    lines = file.readlines()
    old_url = lines[0].strip()  # 读取第一行并去除换行符

# 初始化 OpenAI 客户端
client = OpenAI(api_key="apikey 自己填入，注意不要带有空格", base_url="https://api.deepseek.com")

# 系统提示词
prompt = '''
我会提供给你一个 URL 和使用 Python requests.get 访问该 URL 的 text 内容，你需要根据 text 内容解析该 URL 可能会跳转到的地址。如果有多个跳转地址，请任意选择一个并返回完整的跳转地址。

具体要求如下：
将其转换为完整的 URL 后直接返回。
输出时只输出结果，不要有任何多余内容。
'''

# 循环处理 URL
for i in range(5):
    r = requests.get(url=old_url)
    input_text = f"url:{old_url} \n text:{r.text}"
    
    # 如果 text 中包含 "forum.php"，则停止循环
    if "forum.php" in r.text:
        break
    
    # 调用 OpenAI API 解析跳转地址
    response = client.chat.completions.create(
        model="deepseek-chat",
        max_tokens=8192,
        temperature=1.3,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": input_text},
        ],
        stream=False
    )
    
    # 打印此次循环的花费和结果
    print("此次循环花费token数:", response.usage.total_tokens)
    print("下一次跳转url:", response.choices[0].message.content)
    
    # 更新 old_url
    old_url = response.choices[0].message.content

# 输出最终结果
print("搜书吧新url:", old_url)

# 将最后更新的 old_url 写回 config.txt 的第一行
lines[0] = old_url + "\n"  # 更新第一行
with open("config.txt", "w", encoding="utf-8") as file:
    file.writelines(lines)  # 写回文件
