s1 = "paraparaparadise"
s2 = "paragraph"

def n_gram(sequence, n):
    return [sequence[i:i + n] for i in range(len(sequence) - n + 1)]

X = set(n_gram(s1, 2))
Y = set(n_gram(s2, 2))

union_set = X | Y       
intersection_set = X & Y
difference_X_Y = X - Y

se_in_X = 'se' in X
se_in_Y = 'se' in Y

file_name = '06.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(f"X (paraparaparadise): {X}\n")
    f.write(f"Y (paragraph):        {Y}\n")

    f.write(f"和集合 (X ∪ Y):       {union_set}\n")
    f.write(f"積集合 (X ∩ Y):       {intersection_set}\n")
    f.write(f"差集合 (X \\ Y):       {difference_X_Y}\n")
    
    f.write(f"'se'はXに含まれる:  {se_in_X}\n")
    f.write(f"'se'はYに含まれる:  {se_in_Y}\n")
