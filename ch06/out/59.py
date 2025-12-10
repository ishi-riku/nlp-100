import numpy as np
from gensim.models import KeyedVectors
import sys
import pycountry
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

# 1. モデルのロード
MODEL_FILE_PATH = 'GoogleNews-vectors-negative300.bin.gz'
try:
    vectors = KeyedVectors.load_word2vec_format(MODEL_FILE_PATH, binary=True)
except:
    print(f"エラー: モデルファイル '{MODEL_FILE_PATH}' のロードに失敗しました。")
    sys.exit(1)

# 2. 国名ベクトルの抽出
all_countries = list(pycountry.countries)
country_vectors = []
country_words = []

for country in all_countries:
    # Word2Vec形式に変換し、一般的な国名のみを対象とする
    word = country.name.replace(' ', '_')
    if word in vectors and 4 <= len(word) <= 30 and word.count('_') <= 3:
        country_vectors.append(vectors[word])
        country_words.append(word)

X = np.array(country_vectors)

if not country_vectors:
    print("エラー: 抽出されたベクトルがありません。")
    sys.exit(1)

# 3. t-SNEによる次元削減
# random_state=42で結果の再現性を確保
tsne = TSNE(n_components=2, perplexity=30, max_iter=3000, random_state=42, learning_rate='auto')
X_tsne = tsne.fit_transform(X)

# 4. 結果の可視化と保存
plt.figure(figsize=(20, 15))
plt.scatter(X_tsne[:, 0], X_tsne[:, 1], s=10)

# 国名ラベルの追加
for i, word in enumerate(country_words):
    # アンダースコアをスペースに戻して表示
    display_word = word.replace('_', ' ')
    plt.annotate(display_word, (X_tsne[i, 0], X_tsne[i, 1]), fontsize=8, alpha=0.7)

plt.title('t-SNE Visualization of Country Word Vectors', fontsize=20)
plt.savefig("country_tsne_visualization_simple.png", dpi=300, bbox_inches='tight')
print("t-SNEによる可視化結果を '59.png' に保存しました。")
