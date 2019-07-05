import random


def build_struct(gram):
    """
        左边key为可扩展，右边value为列表，若可扩展则递龟继续扩展，否则直接输出
    :param gram:
    :param target:
    :return:
    """
    struct = {}
    lines = gram.split("\n")
    for line in lines:
        if not line.strip():
            continue
        exp, stmt = line.split("=>")
        struct[exp.strip()] = [s.split() for s in stmt.split("|")]
    return struct


def generate(struct, target):
    choice = random.choice
    if target not in struct:
        return target
    ch = choice(struct[target])
    li = (generate(struct, t) for t in ch)
    str = "".join(li)
    return str


def generate_n(struct, target, n):
    list = []
    for i in range(n):
        list.append(generate(struct, target))
    return list


if __name__ == '__main__':
    quiz_grammar = '''
            quiz => 语气词 介词 动词 形容语句 名词
            语气词 => 什么 | 为什么 | 怎样 
            副词 => 是 | 要 | 有 | 才 | 能
            动词 => 买 | 用 | 卖 | 来
            形容语句 => 形容词 | 量词 形容词
            量词 => 一个 | 一份 
            形容词 => 便宜的 | 合适的 | 昂贵的 | 垃圾的 
            名词 => 人寿保险 | 车险 | 财险 
            '''
    print(generate_n(struct=build_struct(quiz_grammar), target="quiz", n=10))
