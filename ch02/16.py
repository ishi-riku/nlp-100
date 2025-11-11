import os
import random

def shuffle_file_lines(input_filename="popular-names.txt", output_dir="out_py"):

    input_path = input_filename
    output_path = os.path.join(output_dir, "16.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. 全行をリストとして読み込む
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 2. リストの要素（各行）をランダムに並び替える
        random.shuffle(lines)
        
        # 3. 結果を出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(lines)
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    shuffle_file_lines()
