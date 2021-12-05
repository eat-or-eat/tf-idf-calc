import os
import jieba
from tfidf_calc import calc_tfidf


def search_query(tfidf, query, texts):
    query_words = jieba.lcut(query)
    res = []
    for index, words in tfidf.items():
        score = 0
        for word in query_words:
            score += words.get(word, 0)
        res.append([index, score])
    res = sorted(res, key=lambda x: x[1], reverse=True)
    for i in range(2):
        index = res[i][0]
        print(texts[index])
        print("--------------")
    return res


def main():
    dir_path = './data'
    corpus = []
    texts = []
    for text in os.listdir(dir_path):
        path = os.path.join(dir_path, text)
        if path.endswith('.txt'):
            corpus.append(open(path, encoding='utf8').read())
            texts.append(os.path.basename(path))
    temp = [jieba.lcut(text) for text in corpus]
    tfidf = calc_tfidf(temp)
    while True:
        query = input('请输入搜索内容:')
        search_query(tfidf, query, texts)


if __name__ == "__main__":
    main()
