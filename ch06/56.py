import numpy as np
from gensim.models import KeyedVectors
from scipy.stats import spearmanr
import sys
import zipfile
import csv
import io 

# 1. モデルのロード
MODEL_FILE_PATH = 'GoogleNews-vectors-negative300.bin.gz'

try:
    print(f"単語ベクトルファイル '{MODEL_FILE_PATH}' のロード中")
    # KeyedVectors.load_word2vec_format() を使用してファイルを読み込む
    vectors = KeyedVectors.load_word2vec_format(MODEL_FILE_PATH, binary=True)
    print("モデルのロードが完了しました。")
    
except FileNotFoundError:
    print(f"エラー: Word2Vecモデルファイル '{MODEL_FILE_PATH}' が見つかりません。")
    sys.exit(1)
except Exception as e:
    print(f"モデルロード中にエラーが発生しました: {e}")
    sys.exit(1)
    
print("-" * 40)

# 2. WordSimilarity-353データセットの読み込み (ZIPファイル内の combined.csv )
ZIP_FILE_PATH = 'wordsim353.zip'
DATA_FILE_IN_ZIP = 'combined.csv' 

human_scores_raw = []
word_pairs = []

try:
    with zipfile.ZipFile(ZIP_FILE_PATH, 'r') as zf:
        print(f"ZIPファイル '{ZIP_FILE_PATH}' を開きました。")
        
        with zf.open(DATA_FILE_IN_ZIP) as f:
            # バイナリデータを文字列としてデコードし、csvリーダーに渡す
            text_data = io.TextIOWrapper(f, encoding='utf-8')
            reader = csv.reader(text_data)
            
            # ヘッダー行をスキップ
            next(reader) 

            # データを抽出
            for row in reader:
                word1 = row[0]
                word2 = row[1]
                # 3列目が人間評価スコア
                score = float(row[2]) 
                
                word_pairs.append((word1, word2))
                human_scores_raw.append(score)
    
except FileNotFoundError:
    print(f"エラー: 指定されたZIPファイル '{ZIP_FILE_PATH}' が見つかりません。")
    sys.exit(1)
except KeyError:
    print(f"エラー: ZIPファイルの中に '{DATA_FILE_IN_ZIP}' が見つかりません。")
    sys.exit(1)
except Exception as e:
    print(f"ファイルの読み込み中にエラーが発生しました: {e}")
    sys.exit(1)

# 3. 類似度の計算とスコアの抽出
model_scores = []
human_scores = []
missing_pairs = 0

print(f"単語ペア {len(word_pairs)} 組の類似度を計算中")

for i, (word1, word2) in enumerate(word_pairs):
    # 両方の単語がモデルに含まれているか確認
    if word1 in vectors and word2 in vectors:
        # コサイン類似度を計算
        model_score = vectors.similarity(word1, word2)
        
        # モデルスコアと対応する人間スコアを格納
        model_scores.append(model_score)
        human_scores.append(human_scores_raw[i]) 
    else:
        missing_pairs += 1

# 4. スピアマン相関係数の計算
if len(model_scores) < 2:
    print("エラー: 類似度計算に必要なデータ数（2組以上）が不足しています。")
    sys.exit(1)

# scipy.stats.spearmanr を使用して相関係数を計算
correlation, p_value = spearmanr(model_scores, human_scores)

# 5. 結果の表示
print("-" * 40)
print(f"WordSimilarity-353評価データにおける結果")
print(f"計算に利用した単語ペア数: {len(model_scores)} 組")
print(f"スピアマン相関係数: {correlation:.4f}")
print("-" * 40)
