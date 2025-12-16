import pandas as pd
import zipfile
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

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

# テキスト
train_texts = train_df['sentence'].tolist()
dev_texts = dev_df['sentence'].tolist()
# 真のラベル (y_true)
y_train_true = train_df['label'].astype(int).tolist() 
y_dev_true = dev_df['label'].astype(int).tolist() 

# 特徴量ベクトルへの変換と学習
vectorizer = CountVectorizer()
X_train = vectorizer.fit_transform(train_texts) 
X_dev = vectorizer.transform(dev_texts) # 検証データは学習データの語彙で変換

# モデル学習
model = LogisticRegression(random_state=42, solver='liblinear') 
model.fit(X_train, y_train_true)

# 予測と評価
# 学習データに対する予測
y_train_pred = model.predict(X_train)
# 検証データに対する予測
y_dev_pred = model.predict(X_dev)

# 評価関数
def evaluate(y_true, y_pred):
    # 真のラベルと予測ラベルから評価指標を計算する
    return {
        'Accuracy': accuracy_score(y_true, y_pred),
        'Precision': precision_score(y_true, y_pred),
        'Recall': recall_score(y_true, y_pred),
        'F1-score': f1_score(y_true, y_pred)
    }

# 各データセットで評価を実行
train_metrics = evaluate(y_train_true, y_train_pred)
dev_metrics = evaluate(y_dev_true, y_dev_pred)

# 結果表示
print("--- モデル評価結果 ---")
print("| 指標 | 学習データ (Train) | 検証データ (Dev) |")
print("| :--- | :---: | :---: |")
print(f"| 正解率 (Accuracy) | {train_metrics['Accuracy']:.4f} | {dev_metrics['Accuracy']:.4f} |")
print(f"| 適合率 (Precision) | {train_metrics['Precision']:.4f} | {dev_metrics['Precision']:.4f} |")
print(f"| 再現率 (Recall) | {train_metrics['Recall']:.4f} | {dev_metrics['Recall']:.4f} |")
print(f"| F1スコア (F1-score) | {train_metrics['F1-score']:.4f} | {dev_metrics['F1-score']:.4f} |")