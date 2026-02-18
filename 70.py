import torch
import torch.nn as nn
import numpy as np
from gensim.models import KeyedVectors

# 1. データの読み込み (limitで単語数を決める)
w2v = KeyedVectors.load_word2vec_format('./ch06/out/GoogleNews-vectors-negative300.bin.gz', binary=True, limit=1000000)

# 2. 辞書と埋め込み行列の構築
dim = w2v.vector_size               # 次元数 (d_emb = 300)
v_size = len(w2v.index_to_key) + 1  # 語彙数 (|V| = 単語数 + PAD)

# 埋め込み行列を全ゼロで初期化 (これにより E_0 は自動的にゼロベクトルになる)
matrix = np.zeros((v_size, dim), dtype=np.float32)

w2i = {"<PAD>": 0}  # 単語からIDへの変換辞書
i2w = {0: "<PAD>"}  # IDから単語への変換辞書

# w2vの単語を順に処理 (インデックス1から開始して0行目を予約)
for i, word in enumerate(w2v.index_to_key, start=1):
    matrix[i] = w2v[word]  # i行目に単語ベクトルを格納
    w2i[word] = i          # 単語に対するIDを登録
    i2w[i] = word          # IDに対する単語を登録

# PyTorchで扱えるようにTensor型へ変換
weights = torch.from_numpy(matrix)

# 3. 分類モデルの定義
class Net(nn.Module):
    def __init__(self, weights, n_out):
        super().__init__()
        # 埋め込み層: 作成した行列をロードし、学習させない(freeze)設定にする
        # padding_idx=0 を指定することで、ID:0 (<PAD>) のベクトルは勾配計算から除外される
        self.emb = nn.Embedding.from_pretrained(weights, padding_idx=0)

        # 出力層: 埋め込み次元数(300)からクラス数(n_out)へ変換
        self.fc = nn.Linear(weights.shape[1], n_out)

    def forward(self, x):
        # x: 単語IDが並んだテンソル [バッチサイズ, 文の長さ]
        # 各単語IDをベクトルへ変換 -> [batch, seq_len, 300]
        e = self.emb(x)

        # 文のベクトルを作る (各単語ベクトルの平均をとる) -> [batch, 300]
        # dim=1(文の長さ方向)で平均をとる(Global Average Pooling)
        pooled = e.mean(dim=1)

        # 3. 全結合層に通して各クラスのスコアを出力 -> [batch, n_out]
        return self.fc(pooled)

# 実行例
# 4クラス分類モデルを作成
model = Net(weights, n_out=4)

# 確認
print(f"語彙数: {v_size}, 次元数: {dim}")
print(f"PADベクトルの確認 (先頭5要素): {weights[0][:5]}") # 全て 0.0 のはず
