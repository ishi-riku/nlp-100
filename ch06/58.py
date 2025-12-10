# pip install scipy matplotlib
import numpy as np
from gensim.models import KeyedVectors
import sys
import pycountry  # 国名リストの取得
import warnings
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.pyplot as plt

# 警告を非表示にする
warnings.filterwarnings('ignore')

# 1. モデルのロード設定
MODEL_FILE_PATH = 'GoogleNews-vectors-negative300.bin.gz'

print("-" * 40)
print("処理を開始します")

# モデルのロード
try:
    print(f"単語ベクトルファイル '{MODEL_FILE_PATH}' をロード中")
    vectors = KeyedVectors.load_word2vec_format(MODEL_FILE_PATH, binary=True)
    print("モデルのロードが完了しました。")
    
except FileNotFoundError:
    print(f"エラー: Word2Vecモデルファイル '{MODEL_FILE_PATH}' が見つかりません。")
    sys.exit(1)
except Exception as e:
    print(f"モデルロード中にエラーが発生しました: {e}")
    sys.exit(1)

# 2. pycountryから一般名のみを抽出し、ベクトルを取得する関数定義
def get_clean_country_names(country_list):
    """
    pycountryのリストから、Word2Vecの慣習に合わせた一般名のみを抽出する。
    ISOコードや長すぎる正式名称を排除する。
    """
    w2v_country_names = set()
    for country in country_list:
        
        name = country.name
        
        # 1. 正式名が長すぎる場合はスキップ
        if len(name) > 30 and hasattr(country, 'official_name') and name == country.official_name:
            continue
            
        # 2. Word2Vec形式に変換 (スペースをアンダースコアに)
        word = name.replace(' ', '_')
        
        # 3. 単語の長さが4文字未満(コードの可能性)、またはアンダースコアが多すぎる単語を排除
        if len(word) < 4 or word.count('_') > 3:
            continue

        w2v_country_names.add(word)
            
    return w2v_country_names

# 3. データの準備とベクトル化

# pycountryから信頼できる国名リストを取得
all_countries = list(pycountry.countries)
target_country_names = get_clean_country_names(all_countries)

country_vectors = []
country_words = []
missing_count = 0

# ターゲットリストとWord2Vecの語彙を照合
for word in target_country_names:
    if word in vectors:
        country_vectors.append(vectors[word])
        country_words.append(word)
    else:
        missing_count += 1

# NumPy配列に変換
X = np.array(country_vectors)

if not country_vectors:
    print("エラー: 抽出された国名のベクトルがありません。")
    sys.exit(1)

print(f"抽出対象の国名数: {len(target_country_names)}")
print(f"ベクトル化できた国名数: {len(country_words)} (欠損: {missing_count})")
print(f"データシェイプ: {X.shape}")
print("-" * 40)

# 4. Ward法による階層型クラスタリングの実行

print("Ward法による階層型クラスタリングを実行中")

# linkage関数でクラスタリングを実行
# method='ward': ウォード法（分散最小化）
# metric='euclidean': ユークリッド距離
linked = linkage(X, method='ward', metric='euclidean')

print("クラスタリング完了。デンドログラムを作成します。")

# 5. デンドログラムによる可視化

# プロットのサイズ設定
# 国名が多いので、高さを大きく(40インチ)確保して文字が重ならないようにする
plt.figure(figsize=(15, 40))

# デンドログラムの描画
dendrogram(
    linked,
    orientation='left',            # 左向き（横書きの国名が読みやすいため）
    labels=country_words,          # 国名ラベル
    distance_sort='descending',    # 距離が遠い順にソート
    show_leaf_counts=True,
    leaf_font_size=10              # フォントサイズ
)

plt.title('Hierarchical Clustering of Countries (Ward\'s Method)', fontsize=20)
plt.xlabel('Distance (Ward)', fontsize=14)
plt.ylabel('Country Name', fontsize=14)
plt.grid(which='major', axis='x', linestyle='--', alpha=0.5) # グリッド線を表示

print("描画完了。ウィンドウを表示します...")
plt.tight_layout() # レイアウトの自動調整
output_filename = "58.png"
print(f"画像ファイル '{output_filename}' に保存しています")
plt.savefig(output_filename, dpi=300, bbox_inches='tight') # dpi=300で高画質保存
print("保存が完了しました。")
