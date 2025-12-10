import numpy as np
from gensim.models import KeyedVectors
from sklearn.cluster import KMeans
import sys
import pycountry # 国名リストの取得
import warnings
warnings.filterwarnings('ignore') # k-meansの警告を非表示にする

# 1. モデルのロード
MODEL_FILE_PATH = 'GoogleNews-vectors-negative300.bin.gz'

try:
    print(f"単語ベクトルファイル '{MODEL_FILE_PATH}' のロード中")
    vectors = KeyedVectors.load_word2vec_format(MODEL_FILE_PATH, binary=True)
    print("モデルのロードが完了しました。")
    
except FileNotFoundError:
    print(f"エラー: Word2Vecモデルファイル '{MODEL_FILE_PATH}' が見つかりません。")
    sys.exit(1)
except Exception as e:
    print(f"モデルロード中にエラーが発生しました: {e}")
    sys.exit(1)

print("-" * 40)


# ------------------------------------------------------------------------------------------
# 2. pycountryから一般名のみを抽出し、ベクトルを取得
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
            
        # 2. Word2Vec形式に変換
        word = name.replace(' ', '_')
        
        # 3. 単語の長さが4文字未満(コードの可能性)、またはアンダースコアが多すぎる単語を排除
        if len(word) < 4 or word.count('_') > 3:
            continue

        w2v_country_names.add(word)
            
    return w2v_country_names

# 1. pycountryから信頼できる国名リストを取得し、一般名に絞り込む
all_countries = list(pycountry.countries)
target_country_names = get_clean_country_names(all_countries)

country_vectors = []
country_words = []
missing_count = 0

# 2. ターゲットリストとWord2Vecの語彙を照合
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

print(f"一般名に絞り込み、抽出された国名: {len(country_words)} 個")
print(f"データシェイプ: {X.shape}")
print("-" * 40)

# 3. k-meansクラスタリングの実行 (k=5)
K = 5
print(f"k-meansクラスタリング (k={K}) を実行中")

kmeans = KMeans(n_clusters=K, random_state=42, n_init='auto')
kmeans.fit(X)

labels = kmeans.labels_

# 4. 結果の出力
cluster_assignments = [[] for _ in range(K)]

for word, label in zip(country_words, labels):
    cluster_assignments[label].append(word)

print("\nk-means クラスタリング結果 (K=5)")
print("-" * 40)

for k in range(K):
    print(f"**クラスタ {k} ({len(cluster_assignments[k])} 項目)**:")
    
    # 全項目を出力
    print(f"  {', '.join(cluster_assignments[k])}")
    print("-" * 40)
