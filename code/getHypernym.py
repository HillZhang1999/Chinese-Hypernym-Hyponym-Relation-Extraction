from bs4 import BeautifulSoup
import requests
import urllib
global count
import time
count=0

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
    web_data = s.get(url,timeout=3)
    web_data.encoding = 'utf-8'
    soup = BeautifulSoup(web_data.text, 'html.parser')
    return soup

def getPage(word):#获取百科页面的地址（可能有多义词）
    url="https://fenlei.baike.com/"+urllib.parse.quote(word)
    soup=getSoup(url)
    for k in soup.find_all(name='title'):  # 抽取词条标签的源代码
        result=(str(k).lstrip('<title xmlns="http://www.w3.org/1999/xhtml">').lstrip('<title>').rstrip('</title>').split(' ')[0].split('_')[0])
        break
    if (result==word):
        return True
    return False

def chooseWordPairs(filename1,filename2):
    li=readFile(filename1)
    dic=readFile('Hypernym.txt')
    dicGL=readFile('dictGL')
    w=open(filename2,'w',encoding='utf-8')
    count=0
    ww=open('count.txt','a+')
    for line in li:
        h1=line.split()[0]
        h2=line.split()[1]
        if (h2 in dic)and(h1 not in dicGL)and(h2 not in dicGL) and(h1 not in h2):
            w.write(line+'\n')
            count+=1
            w.flush()
    print(count)
    ww.write(filename2+':'+str(count)+'\n')
    w.close()

def main():
    #li=readFile('WordPairs-fenlei-v1.txt')
    #result=[]
    #w=open('Hypernym.txt','w',encoding='utf-8')
    #for line in li:
    #    tmp=line.split()[1]
    #    if (tmp not in result):
    #        result.append(tmp)
    #for h in result:
    #    w.write(h+'\n')
    #w.close()
    chooseWordPairs('/Users/hillzhang/Desktop/result/DP_all_sorted.out','/Users/hillzhang/Desktop/result/DP_all_sorted_2.out')
    # 主函数

if __name__ == '__main__':
    main()
#运行主函数