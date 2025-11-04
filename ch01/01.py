s = "パタトクカシーー"

result = ''.join(s[i] for i in (1, 3, 5, 7)) 

file_name = '01.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(result)
