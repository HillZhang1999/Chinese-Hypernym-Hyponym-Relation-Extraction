import LP as father
class LP_include(father.LP):
    def achieve_useful_sentence(self,baike, useful_sentence):
        """
        从语料集合中抽取符合include模式的句子集合
        :param baike: 语料集合
        :param useful_sentence:符合include模式的句子集合
        :return:
        """
        pattern_lst = ["包括", "囊括", "包含", "涵盖"]
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
    def achieve_shangwei_and_xiawei(self,useful_sentence, guolv, shangxiawei_houxuan, tiqu_sentence):
        """
        根据符合include模式的句子集合，抽取出相应的上下位关系候选词对集合
        :param useful_sentence: 符合include模式的句子集合
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
        pattern_lst = ["包括", "囊括", "包含", "涵盖"]
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
                    if (j in sentence_lst):
                        cont = sentence_lst.index(j)
                        if (cont != 0 and sentence_lst[cont - 1] != "(" and sentence_lst[cont - 1] != "（"):
                            qian_lst = sentence_lst[0:cont]
                            hou_lst = sentence_lst[cont + 1:len(sentence_lst)]
                            qian_cixing_lst = sentence_cixing_lst[0:cont]
                            hou_cixing_lst = sentence_cixing_lst[cont + 1:len(sentence_lst)]
                            shangwei_houxuan = achieve_shangwei(qian_lst, qian_cixing_lst, guolv_dic, coo_lst)
                            xiawei_houxuan = achieve_xiawei(hou_lst, hou_cixing_lst, guolv_dic, coo_lst)
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

    def achieve_xiawei(self,hou_lst, hou_cixing_lst, guolv_dic, coo_lst):
        """
        重写父类中抽取下位词的算法，根据后串词列表和词性列表抽取相应的下位词
        :param hou_lst: 分割以后的后串词列表
        :param hou_cixing_lst: 分割以后的后串词性列表
        :param guolv_dic: 过滤词典
        :param coo_lst: 并列词列表
        :return:
        """
        xiawei_houxuan = []
        for i in guolv_dic:
            if (i in hou_lst):
                return xiawei_houxuan
        tep_lst = hou_lst
        shuminghao_count = []
        for i in range(len(tep_lst) - 1):
            if (tep_lst[i] == "《"):
                for j in range(i + 1, len(tep_lst)):
                    if (tep_lst[j] == "》"):
                        shuminghao_count.append([i, j])
                        break
        if ("的" in hou_lst):
            hou_lst = hou_lst[::-1]
            hou_cixing_lst = hou_cixing_lst[::-1]
            cot = hou_lst.index("的")
            if (cot + 1 < len(hou_lst) and hou_cixing_lst[cot + 1] == "PN"):
                return xiawei_houxuan
            hou_lst = hou_lst[0:cot]
            hou_cixing_lst = hou_cixing_lst[0:cot]
            hou_lst = hou_lst[::-1]
            hou_cixing_lst = hou_cixing_lst[::-1]
        cott = 0
        ct = cott
        hou_lst_he = []
        hou_cixing_lst_he = []
        while (cott < len(hou_lst)):
            for m in coo_lst:
                if (m == hou_lst[cott]):
                    hou_lst_he.append(hou_lst[ct:cott])
                    hou_cixing_lst_he.append(hou_cixing_lst[ct:cott])
                    ct = cott + 1
                else:
                    continue
            cott += 1
        hou_lst_he.append(hou_lst[ct:cott])
        hou_cixing_lst_he.append(hou_cixing_lst[ct:cott])
        Replenish = ["有限", "之"]
        DT = ["本", "此", "该", "这"]
        for i in range(len(hou_lst_he)):
            ddt1 = hou_lst_he[i][::-1]
            ddt1_pos = hou_cixing_lst_he[i][::-1]
            if (len(ddt1) > 0):
                if ("LC" in ddt1_pos and "P" in ddt1_pos):
                    lc = ddt1_pos.index("LC")
                    p = ddt1_pos.index("P")
                    if (lc != -1 and p != -1):
                        if (p > lc):
                            temp = ddt1[p + 1:]
                            ddt1 = ddt1[0:lc]
                            for k in temp:
                                ddt1.append(k)
                            temp_lst = ddt1_pos[p + 1:]
                            ddt1_pos = ddt1_pos[0:lc]
                            for k in temp_lst:
                                ddt1_pos.append(k)
                xiawei = ""
                scount = -1
                for i in range(len(ddt1)):
                    if (ddt1_pos[i] == "NN" or ddt1_pos[i] == "NR"):
                        xiawei += ddt1[i]
                        scount = i
                        break
                if (scount != -1):
                    if (len(shuminghao_count) > 0):
                        flag = 1
                        tep_count = tep_lst.index(xiawei)
                        for m in shuminghao_count:
                            if (tep_count < m[1] and tep_count > m[0]):
                                xiawei_lst = tep_lst[m[0] + 1:m[1]]
                                xiawei = "".join(xiawei_lst)
                                flag = 0
                                break
                        if (flag == 1):
                            while (scount + 1 < len(ddt1)):
                                if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                            ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                    scount += 1
                                    xiawei = ddt1[scount] + xiawei
                                elif (scount + 2 < len(ddt1) and ddt1_pos[scount + 1] == "M" and ddt1[
                                        scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                            ddt1_pos[scount + 1] == "PN") or (
                                                        scount + 2 < len(ddt1) and ddt1_pos[scount + 1] == "DEG" and
                                                ddt1_pos[
                                                        scount + 2] == "PN"):
                                    xiawei = ""
                                    break
                                else:
                                    break
                    else:
                        while (scount + 1 < len(ddt1)):
                            if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                scount += 1
                                xiawei = ddt1[scount] + xiawei
                            elif (scount + 2 < len(ddt1) and ddt1_pos[scount + 1] == "M" and ddt1[
                                    scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                ddt1_pos[scount + 1] == "PN") or (
                                            scount + 2 < len(ddt1) and ddt1_pos[scount + 1] == "DEG" and ddt1_pos[
                                    scount + 2] == "PN"):
                                xiawei = ""
                                break
                            else:
                                break
                if (len(xiawei) > 0):
                    xiawei_houxuan.append(xiawei)
        return xiawei_houxuan

    def achieve_shangwei(self,qian_lst, qian_cixing_lst, guolv_dic, coo_lst):
        """
        重写父类中关于抽取上位词的算法，根据分割以后的前串词列表和词性列表抽取上位词
        :param qian_lst: 分割以后的前串词列表
        :param qian_cixing_lst: 分割以后的前串词性列表
        :param guolv_dic: 过滤词典
        :param coo_lst: 并列词列表
        :return:
        """
        shangwei_houxuan = []
        for i in guolv_dic:
            if (i in qian_lst):
                return shangwei_houxuan
        tep_lst = qian_lst
        shuminghao_count = []
        for i in range(len(tep_lst) - 1):
            if (tep_lst[i] == "《"):
                for j in range(i + 1, len(tep_lst)):
                    if (tep_lst[j] == "》"):
                        shuminghao_count.append([i, j])
                        break
        if ("的" in qian_lst):
            qian_lst = qian_lst[::-1]
            qian_cixing_lst = qian_cixing_lst[::-1]
            cot = qian_lst.index("的")
            if (cot + 1 < len(qian_lst) and qian_cixing_lst[cot + 1] == "PN"):
                return shangwei_houxuan
            qian_lst = qian_lst[0:cot]
            qian_cixing_lst = qian_cixing_lst[0:cot]
            qian_lst = qian_lst[::-1]
            qian_cixing_lst = qian_cixing_lst[::-1]
        cott = 0
        ct = cott
        qian_lst_he = []
        qian_cixing_lst_he = []
        while (cott < len(qian_lst)):
            for m in coo_lst:
                if (m == qian_lst[cott]):
                    qian_lst_he.append(qian_lst[ct:cott])
                    qian_cixing_lst_he.append(qian_cixing_lst[ct:cott])
                    ct = cott + 1
                else:
                    continue
            cott += 1
        qian_lst_he.append(qian_lst[ct:cott])
        qian_cixing_lst_he.append(qian_cixing_lst[ct:cott])
        Replenish = ["有限", "之"]
        DT = ["本", "此", "该", "这"]
        for i in range(len(qian_lst_he)):
            ddt1 = qian_lst_he[i][::-1]
            ddt1_pos = qian_cixing_lst_he[i][::-1]
            if (len(ddt1) > 0):
                flag1 = 0
                if ("LC" in ddt1_pos and "P" in ddt1_pos):
                    lc = ddt1_pos.index("LC")
                    p = ddt1_pos.index("P")
                    if (lc != -1 and p != -1):
                        if (p > lc):
                            temp = ddt1[p + 1:]
                            ddt1 = ddt1[0:lc]
                            for k in temp:
                                ddt1.append(k)
                            temp_lst = ddt1_pos[p + 1:]
                            ddt1_pos = ddt1_pos[0:lc]
                            for k in temp_lst:
                                ddt1_pos.append(k)
                shangwei = ""
                zhongxinci = ""
                scount = -1
                for i in range(len(ddt1)):
                    if (ddt1_pos[i] == "NN" or ddt1_pos[i] == "NR"):
                        shangwei += ddt1[i]
                        zhongxinci = shangwei
                        scount = i
                        break
                if (scount != -1):
                    if (len(shuminghao_count) > 0):
                        flag = 1
                        tep_count = tep_lst.index(shangwei)
                        for m in shuminghao_count:
                            if (tep_count < m[1] and tep_count > m[0]):
                                shangwei_lst = tep_lst[m[0] + 1:m[1]]
                                shangwei = "".join(shangwei_lst)
                                flag = 0
                                break
                        if (flag == 1):
                            while (scount + 1 < len(ddt1)):
                                if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                    ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                    scount += 1
                                    shangwei = ddt1[scount] + shangwei
                                    flag1 = 1
                                elif (scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "M" and ddt1[
                                        scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                    ddt1_pos[scount + 1] == "PN") or (
                                                scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "DEG" and
                                        ddt1_pos[scount + 2] == "PN"):
                                    shangwei = ""
                                    break
                                else:
                                    break

                    else:
                        while (scount + 1 < len(ddt1)):
                            if (ddt1_pos[scount + 1] == "NN") or (ddt1_pos[scount + 1] == "NR") or (
                                ddt1_pos[scount + 1] == "CD") or (ddt1[scount + 1] in Replenish):
                                scount += 1
                                shangwei = ddt1[scount] + shangwei
                                flag1 = 1
                            elif (scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "M" and ddt1[
                                    scount + 2] in DT) or (ddt1[scount + 1] in DT) or (
                                ddt1_pos[scount + 1] == "PN") or (
                                            scount + 2 < len(ddt1_pos) and ddt1_pos[scount + 1] == "DEG" and ddt1_pos[
                                    scount + 2] == "PN"):
                                shangwei = ""
                                break
                            else:
                                break
                if (len(shangwei) > 0):
                    shangwei_houxuan.append(shangwei)
                if (flag1 == 1 and len(zhongxinci) > 0):
                    shangwei_houxuan.append(zhongxinci)

        return shangwei_houxuan