def cipher(text):
  
    # 英小文字を (219 - 文字コード) の文字に置換し、それ以外の文字はそのままにする関数
    result = ""
    
    for char in text:
        if 'a' <= char <= 'z':
            # charの文字コードを取得
            char_code = ord(char)
            
            # 置換を適用
            new_code = 219 - char_code
            
            # 3. 変換後の文字コードから文字を取得し、追加
            new_char = chr(new_code)
            result += new_char
        else:
            result += char
            
    return result

s = "I am an NLPer."

# 1. 暗号化
encrypted_s = cipher(s)

# 2. 復号化
decrypted_s = cipher(encrypted_s)

file_name = '08.txt'
with open(file_name, 'w', encoding='utf-8') as f:
    f.write(f"暗号化: {encrypted_s}\n")
    f.write(f"復号化: {decrypted_s}\n")
