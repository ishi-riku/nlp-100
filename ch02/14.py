import itertools
import os

def extract_first_column(n=10, input_filename="popular-names.txt", output_dir="out_py"):
    
    input_path = input_filename
    output_path = os.path.join(output_dir, "14.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. ファイルから先頭 N 行を読み込む
        with open(input_path, 'r', encoding='utf-8') as f:
            head_lines = itertools.islice(f, n)
            
            extracted_data = []
            for line in head_lines:
                # 行をタブで分割し、1列目 を取得
                columns = line.split('\t')
                first_column = columns[0]
                extracted_data.append(first_column + '\n') # 改行を追加してリストに追加
        
        # 2. 結果を出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(extracted_data)
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    extract_first_column(n=10)
