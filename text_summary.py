import os
import re
import json
import jieba
from tfidf_calc import calc_tfidf

# 计算摘要语句
def calc_summary(tfidf, corpus, K=3):
    res = []
    sentences = re.split('。|！|？', corpus)
    for index, sentence in enumerate(sentences):  # 计算每一句话的重要程度
        score = 0
        words = jieba.lcut(sentence)
        for word in words:
            score += tfidf.get(word, 0)
        score /= (len(words) + 1)  # 每一句话需要归一化一次，不然越长越有利
        res.append([index, score])
    res = sorted(res, key=lambda x: x[1], reverse=True)
    res = sorted([x[0] for x in res[:K]])  # 重要句子可能是第3，6，1句，重排成第1，3，6句
    return '。'.join([sentences[index] for index in res])

# 返回所有文本摘要
def res_summary(tfidf_dic, corpus, texts):
    res = []
    for index, words in tfidf_dic.items():  # 遍历每一篇文章
        summary = calc_summary(words, corpus[index])
        if not summary:
            continue
        res.append({'文本名': texts[index], '摘要': summary})
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
    res = res_summary(tfidf, corpus, texts)
    output = open('./text_summary.json', 'w', encoding='utf8')  # 输出展示
    output.write(json.dumps(res, ensure_ascii=False, indent=2))
    output.close()


if __name__ == "__main__":
    main()

