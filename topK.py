import os
import jieba
from tfidf_calc import calc_tfidf


# 利用tfidf显找出个某领域的top关键词,通过降序排序方法获得某领域的topK
def tf_idf_topK(tf_idf_dic, classes=[], K=5, print_word=True):
    topK_dic = {}
    for index, words_dic in tf_idf_dic.items():  # 遍历每个文档
        word_list = sorted(words_dic.items(), key=lambda x: x[1], reverse=True)
        topK_dic[index] = word_list[:K]
        if print_word:
            print(index, classes[index])
            for i in range(K):
                print(word_list[i])
            print('-----------')
    return topK_dic


def main(K=10):
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
    tf_idf_topK(tfidf, classes, K)
    return tfidf


if __name__ == '__main__':
    main()
