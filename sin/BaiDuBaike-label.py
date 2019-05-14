from bs4 import BeautifulSoup
import requests
import re
import urllib
import time
global count
count=80256

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
    web_data = s.get(url,timeout=1)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'html.parser')
    return soup

def getBaiKeUrl(word):#获取百科页面的地址（可能有多义词）
    url="https://baike.baidu.com/item/"+urllib.parse.quote(word)
    soup=getSoup(url)
    result=[url]
    for i in soup.find_all(name='div',class_="lemmaWgt-subLemmaListTitle"):
        for k in soup.find_all(name='li', class_="list-dot list-dot-paddingleft"):  # 抽取多义词标签的源代码
            for link in re.findall(r"href=(.+?)target", str(k)):
                result.append("https://baike.baidu.com"+link.lstrip('"').rstrip('" '))
    for k in soup.find_all(name='ul', class_="polysemantList-wrapper cmn-clearfix"):  # 抽取多义词标签的源代码（考虑不同网页架构）
        for link in re.findall(r"href=(.+?)title", str(k)):
            result.append("https://baike.baidu.com"+link.lstrip('"').rstrip('" '))
    return result

def getLabel(word,urlL):#抽取标签，作为上位,返回上下对列表（上位 下位）
    result=[]
    for url in urlL:
        soup=getSoup(url)
        for k in soup.find_all(name='span', class_="taglist"):  # 抽取词条标签的源代码
            k=str(k).replace('<span class="taglist">','').replace('</span>','').split()[0]#正则表达式抽label
            if(k!="<a"):
                result.append(word+" "+k)
    return result

def saveWordPairs(filename1,filename2,start):#保存基于label的上下位词对,从词典文件的第start个词开始
    global count
    li=readFile(filename1)[start:]
    f=open(filename2,'a+',encoding='utf-8')
    count=start+1
    s=str(len(li))
    wordPais=[]
    for st in li:
        print("保存词对第"+str(count)+"个任务,上位词："+st+",共84742个任务")
        p=getLabel(st,getBaiKeUrl(st))
        for w in p:
            if(w not in wordPais):
                f.write(w+'\n')
                print(w)
                wordPais.append(w)
        count+=1
        f.flush()
    f.close()

def chooseWordPairs(filename1,filename2,dicname):#抽取均在词典中的词对
    f1 = open(filename2, 'w', encoding='utf-8')
    dic=readFile(dicname)
    for s in readFile(filename1):
        wordPairs=s.split()
        flag=0
        for word in wordPairs:
            if (word not in dic):
                flag=1
                break
        if (flag==0):
            print(s)
            f1.write(s+'\n')
            f1.flush()
    f1.close()

def main():
    #chooseWordPairs('WordPairs-label-v1.txt','WordPairs-label-v2.txt','words.conll')
    #global count
    #while (count <= 84742):
    #    try:
    #        saveWordPairs('words.conll', 'WordPairs-label-v1.txt', count - 1)
    #    except:  # 防止异常
    #        print('第' + str(count) + '个任务失败！')
    #        time.sleep(3)
    #        pass
    print(len(readFile('WordPairs-fenlei-v1.txt')))
#主函数

if __name__ == '__main__':
  main()
#运行主函数
