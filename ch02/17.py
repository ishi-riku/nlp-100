import os

def find_first_column(input_filename="popular-names.txt", output_dir="out_py"):
    
    input_path = input_filename
    output_path = os.path.join(output_dir, "17.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    unique_names = set()
    
    try:
        # 1. ファイルを読み込み、1列目をsetに追加して重複を除去
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                # タブ区切りで分割し、1列目を取得
                name = line.split('\t')[0]
                unique_names.add(name)
        
        # 2. 結果をソートし、改行を付けてリスト化
        # sorted()はリストを返す
        sorted_names = sorted(list(unique_names))
        output_lines = [name + '\n' for name in sorted_names]
        
        # 3. 結果を出力
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(output_lines)
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    find_first_column()
