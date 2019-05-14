import struct
import gzip
import jieba
import re

def readFile(filename):  # 读取文件,返回列表
    f = open(filename, 'r', encoding='utf-8')
    st = f.readline()
    result = []
    while (st):
        result.append(st.replace("\n", ""))
        st = f.readline()
    f.close()
    return result

def appendWord(filename,word):#向词典中添词
    f = open(filename, 'a+', encoding='utf-8')
    f.write(word+"\n")
    f.close()

def getValue(word1,word2):#计算筛选值F,F= F=together(a,b)/min(count(a),count(b))，其中together(a,b)为a词和b词在所有语料中在同一个句中出现的次数，count(a)为a词在所有语料中出现的次数
    with open("words.conll", "r", encoding="utf-8")as word_file:
        words = []
        for word in word_file.readlines():
            words.append(word.strip())
    wordNum = len(words)
    id2word_dict = {i: word for (i, word) in enumerate(words)}
    word2id_dict = {word: i for (i, word) in enumerate(words)}

    a = word2id_dict[word1]
    b = word2id_dict[word2]

    a_list = []
    flag_a = 0
    b_list = []
    flag_b = 0

    with open("/Users/hillzhang/Desktop/zhangyue19/wiki/wiki_dict/wiki_data.dict_b", "rb") as data_dict_b:
        while True:
            read_data = data_dict_b.read(4)
            if read_data:
                word_id = struct.unpack('i', read_data)[0]
                if word_id == a:
                    flag_a = 1
                    sentence_len = struct.unpack('i', data_dict_b.read(4))[0]
                    for i in range(sentence_len):
                        a_list.append(struct.unpack('i', data_dict_b.read(4))[0])
                    flag = struct.unpack('i', data_dict_b.read(4))[0]
                    if flag != -1:
                        print("数据出错a")
                        break
                    if flag_b == 1:
                        break
                elif word_id == b:
                    flag_b = 1
                    sentence_len = struct.unpack('i', data_dict_b.read(4))[0]
                    for i in range(sentence_len):
                        b_list.append(struct.unpack('i', data_dict_b.read(4))[0])
                    flag = struct.unpack('i', data_dict_b.read(4))[0]
                    if flag != -1:
                        print("数据出错b")
                        break
                    if flag_a == 1:
                        break
                else:
                    # print(word_id)
                    sentence_len = struct.unpack('i', data_dict_b.read(4))[0]
                    # print(sentence_len)
                    data_dict_b.seek(4 * sentence_len, 1)
                    flag = struct.unpack('i', data_dict_b.read(4))[0]
                    # print(flag)
                    if flag != -1:
                        print("数据出错")
                        break
            else:
                break
    print(len(a_list))
    c_list = sorted(list(set(a_list) & set(b_list)))
    a_list_id = 0
    sentences_list = []

    with gzip.open("/Users/hillzhang/Desktop/zhangyue19/wiki//wiki_data/filter_wiki_data.gz", 'rt', encoding="utf-8") as pf:
        for i, line in enumerate(pf):
            if i == a_list[a_list_id]:
                print(line)
                a_list_id += 1
                if a_list_id == len(a_list):
                    break
    if len(c_list) == 0:
        return 0
    else:
        return (len(c_list)/min(len(a_list),len(b_list)))

def main():
    #for s in readFile('WordPairs-label-v2.txt'):
    #   wordPairs=s.split()
    #    value=getValue(wordPairs[0],wordPairs[1])
    #    if(value>0.08):
    #        print("(" + wordPairs[0] + "," + wordPairs[1] + ")的value为:"+str(value))
    jieba.load_userdict("words.conll")
    f=open('sentenceWithIsA-2.txt','w',encoding='utf-8')
    count=0
    #seg_list = jieba.lcut("他来到了网易杭研大厦", HMM=True)
    #print(seg_list)
    for sentence in (readFile('/Users/hillzhang/Desktop/zhangyue19/wiki/wiki_data/filter_wiki_data')):
        if ('是一' in sentence):
            sentence = re.sub(r'（[^（）]*）', '', sentence)  # 去除解释性的内容
            print("正在写入第"+str(count)+"个任务")
            wordList = jieba.lcut(sentence,HMM=True)
            for word in wordList:
                f.write(word+"/ ")
            f.write('\n')
            count+=1
    f.close()

#主函数

if __name__ == '__main__':
  main()
#运行主函数

