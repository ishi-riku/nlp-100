import pandas as pd
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix

# データ読み込み関数
def load_tsv_from_zip(zf, filename):
    with zf.open(filename) as f:
        return pd.read_csv(f, sep='\t', header=0, quoting=3) 

# データの準備、ベクトル化、モデル学習
ZIP_FILE = 'SST-2.zip'
TRAIN_FILE = 'SST-2/train.tsv'
DEV_FILE = 'SST-2/dev.tsv'

with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    train_df = load_tsv_from_zip(zf, TRAIN_FILE)
    dev_df = load_tsv_from_zip(zf, DEV_FILE)

train_texts = train_df['sentence'].tolist()
dev_texts = dev_df['sentence'].tolist()
# 真のラベル (y_true) を抽出・数値化
y_dev_true = dev_df['label'].astype(int).tolist() 

vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_texts) 
y_train = train_df['label'].astype(int).tolist() 

model = LogisticRegression(random_state=42, solver='liblinear') 
model.fit(X_train, y_train)

# 予測と混同行列の計算

# 検証データの BoW 疎行列を生成 (X_dev)
X_dev = vectorizer.transform(dev_texts) 
# 検証データに対する予測ラベル (y_pred)
y_dev_pred = model.predict(X_dev)

# 混同行列を計算: (真のラベル, 予測ラベル) の順で渡す
conf_matrix = confusion_matrix(y_dev_true, y_dev_pred)

# 結果表示
print("--- 検証データ (dev) に対する混同行列 ---")
# 混同行列はnumpy.ndarrayとして表示される
print(conf_matrix)