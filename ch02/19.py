import os

def sort_by_third_column(input_filename="popular-names.txt", output_dir="out_py"):
    
    input_path = input_filename
    output_path = os.path.join(output_dir, "19.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. 全行をリストとして読み込む
        with open(input_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 2. 3列目の数値（int）をキーとして、降順（reverse=True）でソート
        # - line.split('\t')[2] で3列目の文字列を取得
        # - int(...) で数値に変換
        sorted_lines = sorted(
            lines, 
            key=lambda line: int(line.split('\t')[2]), 
            reverse=True
        )
        
        # 3. 結果を出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(sorted_lines)
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    sort_by_third_column()
