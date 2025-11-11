from collections import deque
import os

def display_tail_n_lines(n=10, input_filename="popular-names.txt", output_dir="out_py"):
    
    input_path = input_filename
    output_path = os.path.join(output_dir, "12.txt")
     
    try:
        # ファイルのイテレータを deque に渡し、末尾 N 行のみを保持
        with open(input_path, 'r', encoding='utf-8') as f:
            tail_lines = deque(f, maxlen=n)
        
        # 結果を出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(tail_lines)
            
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    display_tail_n_lines(n=10)
