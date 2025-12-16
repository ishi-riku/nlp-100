import pandas as pd
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# データ読み込み関数
def load_tsv_from_zip(zf, filename):
    with zf.open(filename) as f:
        return pd.read_csv(f, sep='\t', header=0, quoting=3) 

# データの準備、ベクトル化、モデル学習
ZIP_FILE = 'SST-2.zip'
TRAIN_FILE = 'SST-2/train.tsv'

with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    train_df = load_tsv_from_zip(zf, TRAIN_FILE)

train_texts = train_df['sentence'].tolist()
y_train_true = train_df['label'].astype(int).tolist() 

# 特徴量ベクトルへの変換と学習
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_texts) # 語彙辞書をここで学習
y_train = y_train_true

model = LogisticRegression(random_state=42, solver='liblinear') 
model.fit(X_train, y_train)

# 新しいテキストの予測
TARGET_TEXT = "the worst movie I 've ever seen"

# 入力テキストを特徴ベクトルに変換
# 学習時と同じ vectorizer (語彙辞書) を使用する
X_target = vectorizer.transform([TARGET_TEXT])

# ロジスティック回帰モデルで予測を実行
# predict() は予測ラベル (0 or 1) を返す
predicted_label = model.predict(X_target)[0]

# predict_proba() は各クラスの確率を返す
predicted_proba = model.predict_proba(X_target)[0]

# 結果表示
# ラベルに対応する意味を定義
label_map = {0: "ネガティブ", 1: "ポジティブ"}

print("--- 予測結果 ---")
print(f"入力テキスト: {TARGET_TEXT}")
print(f"予測ラベル: {predicted_label} ({label_map.get(predicted_label)})")
print(f"ポジティブ (1) 確率: {predicted_proba[1]:.4f}")
print(f"ネガティブ (0) 確率: {predicted_proba[0]:.4f}")