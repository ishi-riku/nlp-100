import os
import math

def split_file_by_n_parts(n_parts=10, input_filename="popular-names.txt", output_dir="out_py/15"):

    input_path = input_filename
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # 1. 全行数をカウント
        with open(input_path, 'r', encoding='utf-8') as f:
            total_lines = sum(1 for line in f)
        
        if total_lines == 0:
            print("エラー: ファイルが空です。")
            return
            
        # 2. 1ファイルあたりの行数を計算 (切り上げ)
        lines_per_file = math.ceil(total_lines / n_parts)
        
        # 3. 再度ファイルを読み込み、分割して出力
        with open(input_path, 'r', encoding='utf-8') as f:
            file_index = 0
            
            while True:
                # ファイル名を生成 (xaa, xab, ...)
                suffix = chr(ord('a') + file_index // 26) + chr(ord('a') + file_index % 26)
                output_filename = os.path.join(output_dir, f"x{suffix}")
                
                output_lines = []
                # 1ファイルあたりの行数分を読み込む
                for _ in range(lines_per_file):
                    line = f.readline()
                    if not line:
                        break
                    output_lines.append(line)
                
                if not output_lines:
                    break
                
                # 分割ファイルに書き出し
                with open(output_filename, 'w', encoding='utf-8') as out_f:
                    out_f.writelines(output_lines)
                
                file_index += 1
                
                # N分割が完了したら終了
                if file_index >= n_parts and f.readline() == '':
                     break
                
        
    except FileNotFoundError:
        print(f"エラー: 入力ファイル '{input_path}' が見つかりません。")
    except Exception as e:
        print(f"予期せぬエラー: {e}")

if __name__ == "__main__":
    split_file_by_n_parts(n_parts=10) # 10分割を実行
