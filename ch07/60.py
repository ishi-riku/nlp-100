import pandas as pd
import zipfile

# ZIPファイル内のデータを直接読み込む関数
def load_tsv_from_zip(zf, filename):
    with zf.open(filename) as f:
        # 区切り文字としてタブを指定、0行目をデータ行から除外
        return pd.read_csv(f, sep='\t', header=0, quoting=3) 

ZIP_FILE = 'SST-2.zip'
TRAIN_FILE = 'SST-2/train.tsv'
DEV_FILE = 'SST-2/dev.tsv'

# ZIPファイルを開く
with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    
    # train.tsvの読み込みとカウント
    train_df = load_tsv_from_zip(zf, TRAIN_FILE)
    # 列を位置で指定する .iloc[:, 1]
    labels_series = train_df.iloc[:, 1]  
    # カウントし、インデックス0と1を保証
    train_counts = labels_series.value_counts().reindex([0, 1], fill_value=0).sort_index()

    # dev.tsvの読み込みとカウント
    dev_df = load_tsv_from_zip(zf, DEV_FILE)
    labels_series_dev = dev_df.iloc[:, 1]
    dev_counts = labels_series_dev.value_counts().reindex([0, 1], fill_value=0).sort_index()

# 結果表示
print("--- train.tsv ---")
print(f"ポジティブ (1): {train_counts[1]:,}")
print(f"ネガティブ (0): {train_counts[0]:,}")

print("\n--- dev.tsv ---")
print(f"ポジティブ (1): {dev_counts[1]:,}")
print(f"ネガティブ (0): {dev_counts[0]:,}")