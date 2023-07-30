import requests
import os
address=input("请输入账户地址：")
url="https://api.blockcypher.com/v1/btc/test3/addrs/" +address+"/full?limit=50"
response=requests.get(url)
response.encoding="utf-8"
html=response.text
print("正在获取tx详细信息")
print(html)
f=open("parsed tx data.md","wb")
f.write(html.encode("utf-8"))
f.close()

