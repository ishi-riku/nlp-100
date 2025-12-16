import pandas as pd
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

# データ読み込み関数
def load_tsv_from_zip(zf, filename):
    with zf.open(filename) as f:
        return pd.read_csv(f, sep='\t', header=0, quoting=3) 

# データの準備とモデル学習
ZIP_FILE = 'SST-2.zip'
TRAIN_FILE = 'SST-2/train.tsv'
DEV_FILE = 'SST-2/dev.tsv'

# データの読み込み
with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    train_df = load_tsv_from_zip(zf, TRAIN_FILE)
    dev_df = load_tsv_from_zip(zf, DEV_FILE)

train_texts = train_df['sentence'].tolist()
dev_texts = dev_df['sentence'].tolist()
y_train_true = train_df['label'].astype(int).tolist() 

# 特徴量ベクトルへの変換と学習
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_texts) # 語彙辞書を学習

model = LogisticRegression(random_state=42, solver='liblinear') 
model.fit(X_train, y_train_true)

# 検証データの最初の事例の条件付き確率を求める

# 検証データの最初の事例を抽出
target_text = dev_texts[0]
target_true_label = dev_df['label'].iloc[0]

# 最初の事例のテキストを特徴ベクトルに変換
# transformにはリスト形式で渡す必要がある
X_target = vectorizer.transform([target_text])

# 条件付き確率 P(y | x) を計算
# predict_proba() は [[P(y=0|x), P(y=1|x)]] の形式で確率の配列を返す
probabilities = model.predict_proba(X_target)[0] 

# 結果表示
print("--- 検証データの最初の事例の条件付き確率 ---")
print(f"事例テキスト: {target_text}")
print(f"真のラベル: {target_true_label}")
print(f"P(ネガティブ | x) = P(y=0 | x): {probabilities[0]:.4f}")
print(f"P(ポジティブ | x) = P(y=1 | x): {probabilities[1]:.4f}")