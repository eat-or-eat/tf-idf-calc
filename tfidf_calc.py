import os
import jieba
import math
from collections import defaultdict


# 计算tfidf值
def calc_tfidf(corpus):
    '''
    传入二维词粒度的列表，返回对应文档的tfidf值
    :param corpus: eg:[['今天','吃','北京烤鸭'],['明天','吃','水','煮鱼'],['后天','不知道','吃什么']]
    :return: eg:{0:{'今天':xx.xx,'吃':xx.xx,'北京烤鸭':xx.xx},1:{'明天':xx.xx...}}
    '''
    # 计算tf|idf所需要的数据
    tf_dic = defaultdict(dict)  # key:文档序号，value:dict,文档中每个词出现的次数
    words_num = {}  # key:文档序号，value:每个文档下的总词数
    idf_dic = defaultdict(set)  # key:词，value:set，文档序号，用于统计某个词在多少个文档中出现过
    for index, words in enumerate(corpus):  # 遍历文档个数
        words_num[index] = 0  # 记录每种文档的总词数
        for word in words:  # 遍历每个词
            if word not in tf_dic[index]:  # 如果词不存在则新建dict，词频率加一
                tf_dic[index][word] = 0
            tf_dic[index][word] += 1
            words_num[index] += 1
            idf_dic[word].add(index)
    # 计算tfidf词权重
    tf_idf_dic = defaultdict(dict)
    for index, words_dic in tf_dic.items():
        for word, word_count in words_dic.items():
            tf_idf_dic[index][word] = word_count / words_num[index] * math.log(len(tf_dic) / (len(idf_dic[word]) + 1))
    return tf_idf_dic




def main():
    dir_path = "./data"
    corpus = []
    classes = []
    for path in os.listdir(dir_path):
        path = os.path.join(dir_path, path)
        if path.endswith("txt"):
            corpus.append(open(path, encoding="utf8").read())
            classes.append(os.path.basename(path))
    corpus = [jieba.lcut(text) for text in corpus]
    tfidf = calc_tfidf(corpus)
    return tfidf


if __name__ == "__main__":
    get_tfidf_dic = main()
    print(get_tfidf_dic)
