def template(x, y, z):
    return f"{x}時の{y}は{z}"

result = template(12, "気温", 22.4)

file_name = '07.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(result + "\n")
