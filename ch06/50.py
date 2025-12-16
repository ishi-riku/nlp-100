# pip install gensim
import gzip
from gensim.models import KeyedVectors

# 1. ファイルパスの設定
file_path = 'GoogleNews-vectors-negative300.bin.gz'

# 2. 学習済み単語ベクトルのロード
print("単語ベクトルファイルのロード中")

try:
    # KeyedVectors.load_word2vec_format()を使用してファイルを読み込む。
    model = KeyedVectors.load_word2vec_format(
        file_path, 
        binary=True
        # binary=True: バイナリ形式を指定
    )
    print("ロードが完了しました。")

except FileNotFoundError:
    print(f"エラー: 指定されたファイル '{file_path}' が見つかりません。")
    exit()

# 3. "United_States"の単語ベクトル表示
target_word = "United_States"

# 単語ベクトルを取得して表示
if target_word in model:
    vector = model[target_word]
    
    print("-" * 40)
    print(f"ターゲットの単語: '{target_word}'")
    print(f"ベクトルの次元数: {len(vector)} (300次元)")
    print("単語ベクトル（最初の10個の要素）:")
    # ベクトルの全要素を表示すると長すぎるため、最初の10要素のみを表示
    print(vector[:10]) 
    print("-" * 40)
else:
    print(f"'{target_word}' はモデル内に見つかりませんでした。")
