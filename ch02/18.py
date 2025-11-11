import os
from collections import Counter

def analyze_name_frequency(input_filename="popular-names.txt", output_dir="out_py"):

    input_path = input_filename
    output_path = os.path.join(output_dir, "18.txt")
    
    os.makedirs(output_dir, exist_ok=True)
    
    names = []
    
    try:
        # 1. ファイルを読み込み、1列目の名前をリストに格納
        with open(input_path, 'r', encoding='utf-8') as f:
            for line in f:
                name = line.split('\t')[0]
                names.append(name)
        
        # 2. Counterを使って名前の出現頻度をカウント
        name_counts = Counter(names)
        
        # 3. 頻度の降順、名前の昇順でソート
        # most_common()は (要素, カウント) のタプルを頻度降順で返す
        sorted_counts = name_counts.most_common()
        
        # 4. 結果を整形し、出力
        output_lines = [f"{count}\t{name}\n" for name, count in sorted_counts]
        
        with open(output_path, 'w', encoding='utf-8') as out_f:
            out_f.writelines(output_lines)
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    analyze_name_frequency()
