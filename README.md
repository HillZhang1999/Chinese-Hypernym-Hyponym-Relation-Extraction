# 基于模板的中文上下位关系获取

## 文件说明：

### code文件夹：代码文件

#### 基于依存句法模板的抽取脚本
* pattern_Syntactic.py：基于依存句法模板的抽取脚本父类文件
* pattern_Syntactic_contain.py：基于“包含”依存句法模板的抽取脚本
* pattern_Syntactic_isA.py：基于“是一个”依存句法模板的抽取脚本
* pattern_Syntactic_oneOf.py：基于“之一”依存句法模板的抽取脚本
* pattern_Syntactic_deng.py：基于“等”依存句法模板的抽取脚本
#### 基于词法模板的抽取脚本
* pattern_Syntactic.py：基于词法模板的抽取脚本父类文件
* pattern_Syntactic_contain.py：基于“包含”词法模板的抽取脚本
* pattern_Syntactic_isA.py：基于“是一个”词法模板的抽取脚本
* pattern_Syntactic_oneOf.py：基于“之一”词法模板的抽取脚本
* pattern_Syntactic_deng.py：基于“等”词法模板的抽取脚本

### dictionary文件夹：词典文件
* word_pairs_true.txt：高置信度的上下位词对正例集合
* words.conll：上下位词语限定范围词典
* Hypernym.txt：上位词词典
* 其他文件：用于替换模板中占位符的谓语、量词等词典

### data文件夹：数据文件
* new_hypernymy_600-task.txt：首次标注的600个词对（词法模板和句法模板抽取结果的并集）
* hypernymy_mix_dif_600-task.txt：第二次标注的600个词对（词法模板和句法模板抽取结果的差集）
* new_hypernymy_1600-task.txt：用于计算准确度标注的1600个词对

### 工作日志：工作进展

