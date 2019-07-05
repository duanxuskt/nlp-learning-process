import pandas as pd
import jieba
from collections import Counter
import re, string
from assign import assignment_01 as task


def token(s):
    # we will learn the regular expression next course.
    return re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）：]+", "", s)


def prob_1(word, single_total):
    """
        求单个词汇的概率
        单个词出现的概率 = 该词出现的次数 / 词的总个数（or 总字数)？
        eg：
        [('你'，10),('什么',20), ('商业保险',2)]
        P('什么')=20/(10+20+2)=0.625  or   P('什么')=20/(10+2*20+2*3)=0.357
    :param word:
    :return:
    """
    if word in one_word_count.keys():
        # print("单词 %s 出现了 %d 次" % (word, one_word_count[word]))
        return one_word_count[word] / single_total
    else:
        # print("不存在此单词 %s" % word)
        return 1 / single_total


def prob_2(word1, word2, double_total):
    """
    求两个单词的概率
    :param word1:
    :param word2:
    :param double_total:
    :return:
    """
    conjunct = word1 + word2
    if conjunct in two_word_count.keys():
        # print("组合 %s 出现了 %d 次" % (conjunct, two_word_count[conjunct]))
        return two_word_count[conjunct] / double_total
    else:
        # print("不存在此组合 %s" % conjunct)
        return 1 / double_total


def get_probablity(sentence, one_total, two_total):
    """
        求句子的概率
        P(w1 w2 w3 w4)
        = P(w1|w2w3w4) P(w2|w3w4) P(w3|w4) P(w4)
        ≈ P(w1|w2) P(w2|w3) P(w3|w4) P(w4)
        = P(w1w2)/P(w2) * P(w2w3)/P(w3) * P(w3w4)/P(w4) * P(w4)

        eg：
        ['什么','是','昂贵的'.'财产保险']
        P(什么是昂贵的财产保险)
        = P(什么是)/P(是) * P(是昂贵的）/P(昂贵的) * P(昂贵的财产保险)/P(财产保险) * P(财产保险)
        而求P(什么是)需要重新拆分每个句子
    :param sentence:
    :return:
    """
    words = list(jieba.cut(sentence))
    sentence_pro = 1
    for i in range(len(words)):
        if i < len(words) - 1:
            sentence_pro *= (prob_2(words[i], words[i + 1], two_total) / prob_1(words[i + 1], one_total))

    sentence_pro *= prob_1(words[len(words) - 1], one_total)
    return sentence_pro


if __name__ == '__main__':
    content = pd.read_csv("train.txt", header=None, encoding='utf-8', sep="\+\+\$\+\+")
    print(content.head())
    rows = content.iloc[:, 2]
    # print(len(articles))
    sentences = rows.tolist()
    comment = pd.read_csv("movie_comments.csv", header=None, encoding='utf-8')
    print(comment.colums)

    one_word_context = []
    two_word_gram = []
    for sentence in sentences:
        li = list(jieba.cut(token(sentence)))
        one_word_context.extend(li)
        i = 0
        # 你 是 什么 鬼 = 你是 是什么 什么鬼
        while i < len(li) - 1:
            temp = li[i] + li[i + 1]
            two_word_gram.append(temp)
            i += 1

    one_word_count = Counter(one_word_context)
    two_word_count = Counter(two_word_gram)
    # print(words_count.most_common(100))
    one_total = 0
    for count in one_word_count.values():
        one_total += count

    two_total = 0
    for count in two_word_count.values():
        two_total += count

    sample_sentence_1 = "什么是附加商业保险"
    print(get_probablity(sample_sentence_1, one_total, two_total))
    print("=" * 20)
    sample_sentence_2 = "我去特朗普是魔鬼码"
    print(get_probablity(sample_sentence_2, one_total, two_total))

    print("=" * 20)
    quiz_grammar = '''
                quiz => 语气词 副词 动词 形容语句 名词
                语气词 => 什么 | 为什么 | 怎样 
                副词 => 是 | 要 | 有 | 才 | 能
                动词 => 买 | 用 | 卖 | 来
                形容语句 => 形容词 | 量词 形容词
                量词 => 一个 | 一份 
                形容词 => 便宜的 | 合适的 | 昂贵的 | 垃圾的 
                名词 => 人寿保险 | 车险 | 财险 
                '''
    bundle = task.generate_n(struct=task.build_struct(quiz_grammar), target="quiz", n=10)
    for sentence in bundle:
        print(sentence)
        print(get_probablity(sentence, one_total, two_total))
        print("=" * 20)
