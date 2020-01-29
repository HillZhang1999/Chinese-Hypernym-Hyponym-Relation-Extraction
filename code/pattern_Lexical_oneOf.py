import LP as father
class LP_oneof(father.LP):
    def achieve_useful_sentence(self,baike, Vis, Voneof, useful_sentence):
        """
        根据oneof模式，从语料库中获取符合oneof模式的句子集合
        :param baike: 语料集合
        :param Vis: is模板
        :param Voneof: oneof模板
        :param useful_sentence: 符合oneof模式的句子集合
        :return:
        """
        infile1 = open(Vis, 'r', encoding='utf-8')
        Vis_lst = []
        for i in infile1:
            Vis_lst.append(i[0:len(i) - 1])
        infile1.close()
        infile2 = open(Voneof, 'r', encoding='utf-8')
        Voneof_lst = []
        for i in infile2:
            Voneof_lst.append(i[0:len(i) - 1])
        infile2.close()
        pattern_lst = []
        for i in Vis_lst:
            for j in Voneof_lst:
                pattern_lst.append(i + " " + j)
        infile = open(baike, 'r', encoding='utf-8')
        outfile = open(useful_sentence, 'a+', encoding='utf-8')
        for i in infile:
            st = i[0:len(i) - 1].split()
            for j in pattern_lst:
                lt = j.split()
                if (lt[0] in st and lt[1] in st):
                    outfile.write(i)
                    break
                continue
        infile.close()
        outfile.close()

    def achieve_shangwei_and_xiawei(self,useful_sentence, Vis, Voneof, guolv, shangxiawei_houxuan, tiqu_sentence):
        """
        根据符合oneof模式的语句集合，获取上下位关系候选词对集合
        :param useful_sentence: 符合oneof模式的句子集合
        :param Vis: is模板
        :param Voneof: oneof模板
        :param guolv: 过滤词典
        :param shangxiawei_houxuan:上下位关系候选词对集合
        :param tiqu_sentence: 能够抽取出上下位关系候选词对的句子集合
        :return:
        """
        bianhao = 0
        xushu = 0
        guolv_dic = []
        coo_lst = ["、", "或者", "或", "和", "以及", "与", "及"]
        infile_guolv = open(guolv, 'r', encoding='utf-8-sig')
        for i in infile_guolv:
            guolv_dic.append(i[0:len(i) - 1])
        infile_guolv.close()
        infile = open(useful_sentence, 'r', encoding='utf-8')
        infile1 = open(Vis, 'r', encoding='utf-8')
        Vis_lst = []
        for i in infile1:
            Vis_lst.append(i[0:len(i) - 1])
        infile1.close()
        infile2 = open(Voneof, 'r', encoding='utf-8')
        Voneof_lst = []
        for i in infile2:
            Voneof_lst.append(i[0:len(i) - 1])
        infile2.close()
        pattern_lst = []
        for i in Vis_lst:
            for j in Voneof_lst:
                pattern_lst.append(i + " " + j)
        for i in infile:
            xushu += 1
            st = i[0:len(i) - 1]
            ls = st.split()
            count = (len(ls) // 2)
            fen_ci_lst = ls[0:count]
            ci_xing_lst = ls[count:len(st)]
            every_sentence_lst, every_sentence_cixing_lst = achieve_split_lst(fen_ci_lst, ci_xing_lst)
            shangxiawei_houxuan_lst = []
            for k in range(len(every_sentence_lst)):
                sentence_lst = every_sentence_lst[k]
                sentence_cixing_lst = every_sentence_cixing_lst[k]
                for j in pattern_lst:
                    lt = j.split()
                    if (lt[0] in sentence_lst and lt[1] in sentence_lst):
                        count1 = sentence_lst.index(lt[0])
                        count2 = sentence_lst.index(lt[1])
                        if (count1 < count2 and count1 + 1 != count2):
                            if (sentence_lst[count2] == "之一") or (
                                    sentence_lst[count2] != "之一" and count2 == len(sentence_lst) - 1):
                                qian_lst = sentence_lst[0:count1]
                                hou_lst = sentence_lst[count1 + 1:count2]
                                qian_cixing_lst = sentence_cixing_lst[0:len(qian_lst)]
                                hou_cixing_lst = sentence_cixing_lst[count1 + 1:count2]
                                shangwei_houxuan = achieve_shangwei(hou_lst, hou_cixing_lst, guolv_dic, coo_lst)
                                xiawei_houxuan = achieve_xiawei(qian_lst, qian_cixing_lst, guolv_dic, coo_lst)
                                if (len(shangwei_houxuan) > 0 and len(xiawei_houxuan) > 0):
                                    for m in shangwei_houxuan:
                                        for n in xiawei_houxuan:
                                            if (m != n):
                                                shangxiawei_houxuan_lst.append(n + " " + m)
                                break
            if (len(shangxiawei_houxuan_lst) > 0):
                outfile_juzi = open(tiqu_sentence, 'a+', encoding='utf-8')
                outfile_juzi.write(i)
                bianhao += 1
                outfile_juzi.close()
                print("目前已经扫描了" + str(xushu) + "句，能够提取出上下位关系的句子有" + str(bianhao) + "句，其上下位候选词对如下：")
                outfile_shangxiawei = open(shangxiawei_houxuan, 'a+', encoding='utf-8')
                for mm in shangxiawei_houxuan_lst:
                    outfile_shangxiawei.write(mm + " " + str(bianhao) + "\n")
                    print(mm + " " + str(bianhao))
                outfile_shangxiawei.close()
            else:
                print("目前已经扫描了" + str(xushu) + "句，该句不能提取出上下位关系")
        infile.close()