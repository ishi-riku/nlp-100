def n_gram(sequence, n):
    #与えられたシーケンスからn-gramを生成する関数。
    #n (int): n-gramのサイズ（2ならbi-gram、3ならtri-gram）

    # 連続するn個をスライスして取り出す
    n_grams = [sequence[i:i + n] for i in range(len(sequence) - n + 1)]
    return n_grams

s = "I am an NLPer"

s_replaced = s.replace(" ", "")

char_trigrams = n_gram(s_replaced, 2)

word_sequence = s.split()
word_bigrams = n_gram(word_sequence, 2)

file_name = '05.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(str(char_trigrams) + "\n\n")
    f.write(str(word_bigrams) + "\n")
