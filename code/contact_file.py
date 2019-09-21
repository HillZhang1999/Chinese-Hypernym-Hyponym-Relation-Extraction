n=input('请输入pattern:')
f=open('Sentence_WordPairs_ycjf_'+n+'_baike0_profix_inDic.txt','r',encoding='utf-8')
w=open('Sentence_WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','a+',encoding='utf-8')
count=0
sen=f.readline()
while(len(sen)>0):
    w.write(sen)
    sen=f.readline()
    count+=1
f.close()
w.close()
f=open('WordPairs_ycjf_'+n+'_baike0_profix_inDic.txt','r',encoding='utf-8')
w=open('WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','a+',encoding='utf-8')
sen=f.readline()
while(len(sen)>0):
    w.write(sen)
    sen=f.readline()
f.close()
w.close()
f=open('WordPairs_ycjf_'+n+'_baike1_profix_inDic.txt','r',encoding='utf-8')
w=open('WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','a+',encoding='utf-8')
sen=f.readline()
while(len(sen)>0):
    li=sen.rstrip("\n").split(' ')
    li[2]=int(li[2])+count
    w.write(li[0]+' '+li[1]+' '+str(li[2])+'\n')
    sen=f.readline()
f.close()
w.close()
f=open('Sentence_WordPairs_ycjf_'+n+'_baike1_profix_inDic.txt','r',encoding='utf-8')
w=open('Sentence_WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','a+',encoding='utf-8')
sen=f.readline()
while(len(sen)>0):
    w.write(sen)
    sen=f.readline()
    count+=1
f.close()
w.close()
f=open('WordPairs_ycjf_'+n+'_baike2_profix_inDic.txt','r',encoding='utf-8')
w=open('WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','a+',encoding='utf-8')
sen=f.readline()
while(len(sen)>0):
    li=sen.rstrip("\n").split(' ')
    li[2]=int(li[2])+count
    w.write(li[0]+' '+li[1]+' '+str(li[2])+'\n')
    sen=f.readline()
f.close()
w.close()
f=open('Sentence_WordPairs_ycjf_'+n+'_baike2_profix_inDic.txt','r',encoding='utf-8')
w=open('Sentence_WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','a+',encoding='utf-8')
sen=f.readline()
while(len(sen)>0):
    w.write(sen)
    sen=f.readline()
    count+=1
f.close()
w.close()
count=0
f=open('WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','r',encoding='utf-8')
for line in f:
    count+=1
print("词对数:"+str(count))
count=0
f=open('Sentence_WordPairs_ycjf_'+n+'_baike_profix_inDic.txt','r',encoding='utf-8')
for line in f:
    count+=1
print("句子数:"+str(count))