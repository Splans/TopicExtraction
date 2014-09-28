#encoding=utf-8
import pdb
import sys

sys.path.append("../")

import jieba
# fr = open('testCutWords.txt','r')
# for line in fr:
# 	line = jieba.cut(line,cut_all=False)
# 	line = ' '.join(l for l in line)
# 	print line
# 	fw = open('testCutWords_results.txt','w')
# 	fw.write(str(line)+'\n')
# 	fw.close()

# fw.close()


seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
print "Full Mode:", "/ ".join(seg_list)  # 全模式

seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
print "Default Mode:", "/ ".join(seg_list)  # 默认模式

seg_list = jieba.cut("他来到了网易杭研大厦")
print ", ".join(seg_list)

seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
print ", ".join(seg_list)
