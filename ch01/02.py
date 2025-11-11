s = "stressed"

result = s[::-1]

file_name = '02.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(result)
