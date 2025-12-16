import pandas as pd
import zipfile
from sklearn.feature_extraction.text import CountVectorizer

# データ読み込み関数
def load_tsv_from_zip(zf, filename):
    with zf.open(filename) as f:
        return pd.read_csv(f, sep='\t', header=0, quoting=3) 

ZIP_FILE = 'SST-2.zip'
TRAIN_FILE = 'SST-2/train.tsv'
DEV_FILE = 'SST-2/dev.tsv'

# データの読み込み
with zipfile.ZipFile(ZIP_FILE, 'r') as zf:
    train_df = load_tsv_from_zip(zf, TRAIN_FILE)
    dev_df = load_tsv_from_zip(zf, DEV_FILE)

# テキストとラベルを抽出
train_texts = train_df['sentence'].tolist()
train_labels = train_df['label'].tolist()
dev_texts = dev_df['sentence'].tolist()
dev_labels = dev_df['label'].tolist()

# CountVectorizerの初期化と学習
# デフォルトでスペース区切りでトークン化される
vectorizer = CountVectorizer()
# 学習データを用いて辞書を作成し、特徴ベクトルに変換
train_features_matrix = vectorizer.fit_transform(train_texts)
# 検証データも同じ辞書を使って特徴ベクトルに変換
dev_features_matrix = vectorizer.transform(dev_texts)

# 特徴ベクトル（疎行列）をBoW辞書形式に変換し、辞書リストを生成
def to_dict_list(texts, labels, feature_matrix, vectorizer):
    # テキスト、ラベル、特徴行列から辞書オブジェクトのリストを生成する
    feature_names = vectorizer.get_feature_names_out()
    data_list = []
    
    # 疎行列（CSR形式）を行ごとに反復処理
    for i in range(feature_matrix.shape[0]):
        # i行目の非ゼロ要素のインデックスと値を取得
        row = feature_matrix.getrow(i)
        # 疎行列の要素を辞書形式に変換 (特徴名: 出現頻度)
        feature_dict = {
            feature_names[col]: int(row[0, col])
            for col in row.indices
        }
        
        # 最終的な辞書オブジェクトを作成
        data_list.append({
            'text': texts[i],
            'label': str(labels[i]), # ラベルは文字列として格納
            'feature': feature_dict
        })
    return data_list

# 辞書オブジェクトのリストを生成
train_data = to_dict_list(train_texts, train_labels, train_features_matrix, vectorizer)
dev_data = to_dict_list(dev_texts, dev_labels, dev_features_matrix, vectorizer)

# 学習データの最初の事例を目視で確認
print("--- 学習データの最初の事例 ---")
print(train_data[0])