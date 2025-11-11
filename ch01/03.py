s = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."

s_replaced = s.replace(",", "").replace(".", "")

words = s_replaced.split()

counts = []
for word in words:
    counts.append(len(word))

file_name = '03.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(str(counts))
