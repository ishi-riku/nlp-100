import os
import zipfile
import pandas as pd
import torch
import numpy as np
from gensim.models import KeyedVectors

# 1. SST-2.zip の解凍
zip_file = 'SST-2.zip'
if os.path.exists(zip_file):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall('.')

# 2. 単語埋め込みの読み込みと語彙辞書の作成
vec_path = './ch06/out/GoogleNews-vectors-negative300.bin.gz'
w2v = KeyedVectors.load_word2vec_format(vec_path, binary=True, limit=1000000)

# 単語からIDへの辞書を作成 (0番はパディング用に予約)
w2i = {word: i + 1 for i, word in enumerate(w2v.index_to_key)}
w2i["<PAD>"] = 0
print(f"語彙数: {len(w2i)} (PAD含む)")

# --- 3. SST-2データの読み込みと変換関数の定義 ---
def load_and_process_sst2(file_path, w2i):
    """
    TSVファイルを読み込み、語彙に含まれる単語のみをID化。
    空になった事例は除外した辞書オブジェクトのリストを返す。
    """
    df = pd.read_csv(file_path, sep='\t', encoding='utf-8')
    processed_data = []
    
    for _, row in df.iterrows():
        text = str(row['sentence'])
        label = float(row['label'])
        
        # 単語に分割し、語彙(w2i)にあるものだけIDに変換（未知語は無視）
        ids = [w2i[word] for word in text.split() if word in w2i]
        
        # トークン列が空になった事例はスキップ
        if not ids:
            continue
            
        # 指定された形式で辞書を作成
        processed_data.append({
            'text': text,
            'label': torch.tensor([label]),
            'input_ids': torch.tensor(ids, dtype=torch.long)
        })
        
    return processed_data

# --- 4. 実行 ---
print("データの変換中...")
train_data = load_and_process_sst2('SST-2/train.tsv', w2i)
dev_data = load_and_process_sst2('SST-2/dev.tsv', w2i)

# --- 5. 結果の確認 ---
print(f"訓練セット数: {len(train_data)}")
print(f"開発セット数: {len(dev_data)}")

# 事例の表示
if train_data:
    print("\n[事例の確認]")
    example = train_data[0]
    print(f"text: {example['text']}")
    print(f"label: {example['label']}")
    print(f"input_ids: {example['input_ids']}")
