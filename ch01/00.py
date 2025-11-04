s1 = "パトカー"
s2 = "タクシー"

result = ""

for i in range(len(s1)):
    result += s1[i] + s2[i]

file_name = '00.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(result)
