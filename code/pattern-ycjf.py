
def readFile(filename):  # 读取文件,返回列表
    f = open(filename, 'r', encoding='utf-8')
    st = f.readline()
    result = []
    while (st):
        result.append(st.replace("\n", ""))
        st = f.readline()
    f.close()
    return result

dictGL=readFile('dictGL')#过滤词典

def getYCJFTree(string):#获取依存句法树
    li=string.split()
    #print(li)
    for i in range(len(li)):
        if(li[i][0] in ['0','1'])and (li[i+1][0] in ['0','1']) and (li[i+2][0] in ['0','1']):#找出句子分词后的长度
            return [li[:i],li[2*i:3*i],li[4*i:]]#返回列表，有三部分（【分词】，【词性】，【依存句法】）

def getProfix(words,ycjf,cx,now):#获取名词类的修饰词作为前缀，保证上下位词对的准确度和完全度
    result=[]
    profix=''
    for k in ycjf:
        #print(k)
        if (k[0]==now)and(k[2]=='att')and(eval(k[3])>0.5):
            n=int(k[1])
            #print(eval(k[3]))
            #print(cx[n-1])
            #print(words[n-1])
            #if(words[n]  in dictGL):#考虑过滤词典
            #    return -1
            if(cx[n-1]=='NN'or cx[n-1]=='NR'):
                if words[n]!='的':
                    result.append(words[n - 1])
                else:
                    result.append(words[n - 1]+"的")
                #else:
                #    return -1#判断是否有限定关系，如果有就不抽取词对
    for word in result:
        profix+=word
    #print(profix)
    return profix

def tiaoZhengTree(li):#调整树的形式，方便处理
    ycjf=li[2]
    result=[]
    for i in range(len(ycjf)):#调整树
        if ('_'in ycjf[i]):
            result.append(ycjf[i].split('_'))
    return result

def isIsA(words,now):#判断当前的谓语是否满足“是一【个。。】”的形式
    if (int(now)<len(words)):
        if ('是' in words[int(now)-1] and '不' not in words[int(now)-1])and('一' in words[int(now)]):
            return True
    return False

def getSubj(words,ycjf,cx,now):#获取当前谓语弧的主语
    for k in ycjf:
        #print(k)
        if (k[0]==now)and(k[2]=='subj')and(eval(k[3])>0.5):
            n=int(k[1])
            #print(eval(k[3]))
            #print(cx[n-1])
            #print(words[n-1])
            profix=getProfix(words,ycjf,cx,k[1])
            #if (profix==-1):
            #   return -1
            st = profix + words[n - 1]
            return([st.split('的')[-1], cx[n - 1]])
    return -1

def getObj(words,ycjf,cx,now):#获取当前谓语弧的宾语（考虑并列coo）
    result=[]
    for k in ycjf:
        #print(k)
        if (k[0]==now)and(k[2]=='obj')and(eval(k[3])>0.5):
            n=int(k[1])
            now=k[1]
            profix=getProfix(words, ycjf, cx, k[1])
            #if (profix==-1):
            #    return -1
            print(words[n - 1])
            st = profix + words[n - 1]
            #result.append([st, cx[n - 1]])
            result.append([st.split('的')[-1], cx[n - 1]])
            result.append([words[n - 1], cx[n - 1]])

    while True:#找coo
        flag=0
        for k in ycjf:
            if (k[0] == now) and (k[2] == 'coo') and (eval(k[3])>0.5):
                n = int(k[1])
                now = k[1]
                flag = 1
                profix=getProfix(words, ycjf, cx, k[1])
                #if profix == -1:
                #    return -1
                st=profix+words[n - 1]
                #result.append([st,cx[n-1]])
                result.append([st.split('的')[-1],cx[n-1]])
                result.append([words[n - 1], cx[n - 1]])
        if (flag==0):
            return result
    return -1

def getWordPairs(li):#由依存句法树，按照pattern抽取出上下位关系词汇
    words=li[0]#词汇列表
    print(words)
    ycjf=tiaoZhengTree(li)#依存句法树列表
    cx=li[1]#词性列表
    print(cx)
    print(ycjf)
    subj=''#考虑到同主语的情况，先保存主语
    result=[]
    while True:
        flag=0
        for i in range(len(ycjf)):
            tmp=ycjf[i]
            if (tmp[2]=='root')and(eval(tmp[3])>0.5):#谓语做root的情况（需要先找主语）
                #print(tmp[1])
                subj=getSubj(words,ycjf,cx,tmp[1])
                ycjf[i]='visited'#防止重复访问结点
                if (isIsA(words, tmp[1])):
                    flag = 1
                    objs=getObj(words,ycjf,cx,tmp[1])
                    if (subj!=-1)and(objs!=-1):#要求主、宾语均有返回值
                        #if (subj[1]=='NN')or(subj[1]=='NR'):#是否名词（时间名词除外）
                            for word in objs:
                         #       if (word[1]=='NN')or(word[1]=='NR'):
                                    result.append(subj[0]+" "+word[0])
            elif (tmp[2]=='sasubj')and(eval(tmp[3])>0.5):#谓语做sasubj的情况（主语不变）
                ycjf[i] = 'visited'  # 防止重复访问结点
                if (isIsA(words, tmp[1])):
                    flag = 1
                    objs = getObj(words, ycjf,cx, tmp[1])
                    if (subj != -1) and (objs != -1):  # 要求主、宾语均有返回值
                        #if (subj[1] == 'NN') or (subj[1] == 'NR'):  # 是否名词（时间名词除外）
                            for word in objs:
                        #        if (word[1] == 'NN') or (word[1] == 'NR'):
                                    result.append(subj[0] + " " + word[0])
            elif (tmp[2]=='dfsubj')and(eval(tmp[3])>0.5):#谓语做dfsubj的情况（主语需要重新找）
                subj = getSubj(words, ycjf, cx,tmp[1])
                ycjf[i] = 'visited'  # 防止重复访问结点
                if (isIsA(words, tmp[1])):
                    flag = 1
                    objs = getObj(words, ycjf, cx,tmp[1])
                    if (subj != -1) and (objs != -1):  # 要求主、宾语均有返回值
                        #if (subj[1] == 'NN') or (subj[1] == 'NR'):  # 是否名词（时间名词除外）
                            for word in objs:
                        #        if (word[1] == 'NN') or (word[1] == 'NR'):
                                    result.append(subj[0] + " " + word[0])
            elif (tmp[2]=='obj')and(eval(tmp[3])>0.5):#谓语也有可能是宾语
                if(getSubj(words, ycjf, cx,tmp[1])!=-1):
                    subj = getSubj(words, ycjf, cx, tmp[1])
                if (isIsA(words, tmp[1])):
                    flag = 1
                    ycjf[i] = 'visited'  # 防止重复访问结点
                    objs = getObj(words, ycjf,cx, tmp[1])
                    if (subj != -1) and (objs != -1):  # 要求主、宾语均有返回值
                        #if (subj[1] == 'NN') or (subj[1] == 'NR'):  # 是否名词（时间名词除外）
                            for word in objs:
                        #        if (word[1] == 'NN') or (word[1] == 'NR'):
                                    result.append(subj[0] + " " + word[0])
        if (flag==0):#如果树中没有未访问的符合pattern谓语弧，即可返回结果，否则继续迭代
            return result

def is_contain_chinese(check_str):#判断字符串中是否包含中是否含有中文
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def saveWordPairs(infile,outfile):#保存词对
    f=open(outfile,'w',encoding='utf-8')
    li = readFile(infile)
    count=0
    all=[]
    for i in range(len(li)):
        count+=1
        try:
            print('正在执行第'+str(count)+'个任务')
            resultL=getWordPairs(getYCJFTree(li[i]))
            for result in resultL:
                tmp=result.split()
                if (tmp[0]not in dictGL)and(tmp[1]not in dictGL)and(tmp[0]!=tmp[1]):#去除掉词语中在过滤词典中的、上下位相等的
                    if(result not in all):#去重
                        all.append(result)
        except:
            pass
    count=0
    for w in all:
        count+=1
        print('正在写入第' + str(count) + '个任务')
        f.write(w+'\n')
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
    #saveWordPairs('ycjf-isA-V2.txt','WordPairs-isA-ycjf-v7.txt')
    #chooseWordPairs('WordPairs-isA-ycjf-v7.txt','WordPairs-isA-ycjf-v8.txt','words.conll')
    li=readFile('ycjf-isA-V2.txt')
    resultL = getWordPairs(getYCJFTree(li[3401]))
    print(resultL)


#主函数
if __name__ == '__main__':
  main()
#运行主函数
