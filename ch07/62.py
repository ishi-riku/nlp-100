import pandas as pd
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# データ読み込み関数 (再利用)
def load_tsv_from_zip(zf, filename):
    with zf.open(filename) as f:
        return pd.read_csv(f, sep='\t', header=0, quoting=3) 

ZIP_FILE = 'SST-2.zip'
TRAIN_FILE = 'SST-2/train.tsv'

# データの読み込みと準備
with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    train_df = load_tsv_from_zip(zf, TRAIN_FILE)

# 特徴量 (X) とラベル (y) を抽出
train_texts = train_df['sentence'].tolist()
# ラベルはモデル学習のため、数値型 (int) に変換
train_labels = train_df['label'].astype(int).tolist() 

# 2. 特徴量ベクトルへの変換 (BoW 疎行列 X の生成)
vectorizer = CountVectorizer()
# 学習データを用いて語彙を作成し、疎行列に変換 (X_train)
X_train = vectorizer.fit_transform(train_texts) 
# ラベルリストをnumpy配列に変換（scikit-learnの標準的な入力形式）
y_train = train_labels 

# ロジスティック回帰モデルの学習
# モデルの初期化 (C=1.0 は正則化項のデフォルト値)
model = LogisticRegression(random_state=42, solver='liblinear') 
# X_train (BoW疎行列) と y_train (ラベル) を用いてモデルを学習
model.fit(X_train, y_train)

# 学習済みモデルの確認
print("--- ロジスティック回帰モデル ---")
# 語彙サイズと係数の次元を確認
print(f"学習事例数: {X_train.shape[0]:,}")
print(f"特徴量の次元数（語彙サイズ）: {X_train.shape[1]:,}")
# ロジスティック回帰モデルの係数（重み）の形状を確認
# この係数を使って、各単語がポジティブ/ネガティブにどれだけ影響するかを予測する
print(f"学習済み係数（重み）の形状: {model.coef_.shape}")