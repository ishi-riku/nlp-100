import itertools
import os

def replace_tab_with_space(n=10, input_filename="popular-names.txt", output_dir="out_py"):
    
    input_path = input_filename
    output_path = os.path.join(output_dir, "13.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. ファイルから先頭 N 行を読み込む
        with open(input_path, 'r', encoding='utf-8') as f:
            head_lines = itertools.islice(f, n)
            
            # 2. 各行のタブをスペースに置換する
            replaced_lines = [line.replace('\t', ' ') for line in head_lines]
        
        # 3. 結果を出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(replaced_lines)
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    replace_tab_with_space(n=10)
