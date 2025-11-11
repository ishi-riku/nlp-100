import os

def count_lines(input_filename="popular-names.txt", output_filename="out_py/10.txt"):

    input_path = input_filename
    output_path = output_filename
    
    try:
        # ファイルの行数をカウント
        with open(input_path, 'r', encoding='utf-8') as f:
            line_count = sum(1 for line in f)
        
        # 結果を指定ファイルに出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.write(str(line_count) + '\n')
            
        return line_count
    
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
        return -1
    except Exception as e:
        print(f"予期せぬエラー: {e}")
        return -1

# 実行
if __name__ == "__main__":
    count_lines()
