from bs4 import BeautifulSoup
import requests
import re
import urllib

def readFile(filename):  # 读取文件,返回列表
    f = open(filename, 'r', encoding='utf-8')
    st = f.readline()
    result = []
    while (st):
        result.append(st.replace("\n", ""))
        st = f.readline()
    f.close()
    return result

def getSoup(url):#返回soup对象,解析网页源代码
    s = requests.Session()
    s.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'  # 获取头文件
    web_data = s.get(url,timeout=2)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'html.parser')
    return soup

def getNums(word):#获取当前搜索词的结果数目
    url = 'http://www.baidu.com.cn/s?wd=' + urllib.parse.quote("intitle:"+word) + '&pn=0'#获取搜索页面的url
    soup=getSoup(url)
    for k in soup.find_all(name='span', class_="nums_text"):  # 抽取搜索结果条数的源代码
        nums=""
        for n in re.findall(r"\d+\.?\d*",str(k)):
            nums+=n
        result=eval(nums)#字符串转整数
    print(result)
    return result

def getValue(word1,word2):#依据公式计算W值
    return(2*(getNums(word1+"+"+word2))/(getNums(word1)+getNums(word2)))

def main():
    print(getValue('鸭子','自然'))
    print(getValue('廊桥', '地理'))


#主函数

if __name__ == '__main__':
  main()

#运行主函数
