import LP as father
class LP_isA(father.LP):
    def achieve_useful_sentence(self,baike, Vis, Va, useful_sentence):
        """
        根据isA模式筛选出符合isA模式的候选句子集合
        :param baike:语料句子集合
        :param Vis:模板is
        :param Va:模板a
        :param useful_sentence:符合isA模式的候选句子集合
        :return:
        """
        infile1 = open(Vis, 'r', encoding='utf-8')
        Vis_lst = []
        for i in infile1:
            Vis_lst.append(i[0:len(i) - 1])
        infile1.close()
        infile2 = open(Va, 'r', encoding='utf-8')
        Va_lst = []
        for i in infile2:
            Va_lst.append(i[0:len(i) - 1])
        infile2.close()
        pattern_lst = []
        for i in Vis_lst:
            for j in Va_lst:
                pattern_lst.append(" " + i + " 一" + " " + j + " ")
        infile = open(baike, 'r', encoding='utf-8')
        outfile = open(useful_sentence, 'a+', encoding='utf-8')
        for i in infile:
            for j in pattern_lst:
                if (j in i):
                    outfile.write(i)
                    break
            continue
        infile.close()
        outfile.close()

    def achieve_shangwei_and_xiawei(self,useful_sentence, Vis, Va, guolv, shangxiawei_houxuan, tiqu_sentence):
        """
        根据所筛选出来的符合模式的句子，获取上下位词对候选集合
        :param useful_sentence: 符合模式的句子集合
        :param Vis: is模板
        :param Va: a模板
        :param guolv: 过滤词典
        :param shangxiawei_houxuan:上下位候选词对集合
        :param tiqu_sentence: 能够提取出上下位候选词对的句子
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
        infile1 = open(Vis, 'r', encoding='utf-8')
        Vis_lst = []
        for i in infile1:
            Vis_lst.append(i[0:len(i) - 1])
        infile1.close()
        infile2 = open(Va, 'r', encoding='utf-8')
        Va_lst = []
        for i in infile2:
            Va_lst.append(i[0:len(i) - 1])
        infile2.close()
        pattern_lst = []
        for i in Vis_lst:
            for j in Va_lst:
                pattern_lst.append(" " + i + " 一" + " " + j + " ")
        infile = open(useful_sentence, 'r', encoding='utf-8')
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
                stt = " ".join(sentence_lst)
                for j in pattern_lst:
                    s = stt.find(j)
                    if (s != -1):
                        qianchuan = stt[0:s]
                        qian_lst = qianchuan.split()
                        qian_cixing_lst = sentence_cixing_lst[0:len(qian_lst)]
                        hou_lst = sentence_lst[len(qian_lst) + 3:count]
                        hou_cixing_lst = sentence_cixing_lst[len(qian_lst) + 3:count]
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
