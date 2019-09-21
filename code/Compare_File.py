def readFile( filename):  # 读取文件,返回列表
    f = open(filename, 'r', encoding='utf-8')
    st = f.readline()
    result = []
    while (st):
        result.append(st.replace("\n", ""))
        st = f.readline()
    f.close()
    return result

def compare(filename1,filename2):
    li1 = readFile(filename1)
    li2 = readFile(filename2)
    li3=readFile('word_pairs_true.txt')
    li4=readFile('Hypernym.txt')
    for i in range(len(li1)):
        li1[i] = li1[i].split()[0] + ' ' + li1[i].split()[1]
    for i in range(len(li2)):
        li2[i] = li2[i].split()[0] + ' ' + li2[i].split()[1]
    print(list(set(li1).difference(set(li2))))
    #print(list(set(li1).difference(set(li2)).intersection(set(li3))))
    #for w in list(set(li1).difference(set(li2))):
    #    if (w.split()[1] in li4):
    #        print(w)

def main():
    compare('/Users/hillzhang/PycharmProjects/Synactic_extraction/WordPairs_ycjf_contain_wiki_profix_3.txt', '/Users/hillzhang/PycharmProjects/web/WordPairs_ycjf_contain_wiki_profix_3.txt')
#主函数
if __name__ == '__main__':
  main()
#运行主函数