import random

def typoglycemia(text):

    # 単語の先頭と末尾の文字を残し、中央部分をランダムに並び替える関数。
    #（長さ4以下の単語は並び替えを行わない）
    words = text.split()
    pre_result = []
    
    for word in words:
        n = len(word)
        
        # 長さが4以下の単語
        if n <= 4:
            pre_result.append(word)
            continue
            
        # 3. 長さが5以上の単語
        first = word[0]
        last = word[-1]
        
        # スライス [1:-1] は、2番目の文字から、最後から2番目の文字までを取得
        middle = list(word[1:-1])
      
        random.shuffle(middle)
        
        shuffled_middle = "".join(middle)
        
        processed_word = first + shuffled_middle + last
        pre_result.append(processed_word)

    return " ".join(pre_result)

# テストメッセージ
s = "I couldn't believe that I could actually understand what I was reading : the phenomenal power of the human mind ."

# 実行
result = typoglycemia(s)

file_name = '09.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(result + "\n")
