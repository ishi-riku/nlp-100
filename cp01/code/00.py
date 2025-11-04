s1 = "パトカー"
s2 = "タクシー"
result = ''.join(a + b for a, b in zip(s1, s2))

with open('00.txt', 'w', encoding='utf-8') as f:
    f.write(result)
