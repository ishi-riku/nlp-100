s = ("Hi He Lied Because Boron Could Not Oxidize Fluorine. "
     "New Nations Might Also Sign Peace Security Clause. Arthur King Can.")

s_replaced = s.replace(".", "")

words = s_replaced.split()

single_positions = {1, 5, 6, 7, 8, 9, 15, 16, 19}

result = {}

# enumerate(単語, 位置) で、単語とその位置を同時に取得
for idx, word in enumerate(words, start=1):

    if idx in single_positions:
        pre_result = word[0]
    else:
        pre_result = word[:2]

    result[pre_result] = idx

file_name = '04.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(str(result))
