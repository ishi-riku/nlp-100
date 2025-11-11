import itertools
import os

def display_head_n_lines(n=10, input_filename="popular-names.txt", output_filename="out_py/11.txt"):

    input_path = input_filename
    output_path = output_filename
        
    try:
        lines = []
        with open(input_path, 'r', encoding='utf-8') as f:
            # itertools.isliceを使って、ファイルイテレータから最初のN要素だけを取得
            head_lines = itertools.islice(f, n)
            lines = list(head_lines)
        
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(lines)
            
        return lines
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
        return None
    except Exception as e:
        print(f"予期せぬエラー: {e}")
        return None

# 実行（N=10）
if __name__ == "__main__":
    display_head_n_lines(n=10, output_filename="out_py/11.txt")
