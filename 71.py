import zipfile, re, torch, pandas as pd
from gensim.models import KeyedVectors

# 1. 単語ベクトルの読み込み
model_path = './ch06/out/GoogleNews-vectors-negative300.bin.gz'
# .key_to_indexで「単語: ID」の辞書形式を取得
w2v = KeyedVectors.load_word2vec_format(model_path, binary=True, limit=1000000).key_to_index

def load_sst2(zf, filename):
    # ZIPファイル内のTSVファイルを読み込み、ID化とフィルタリングを行う関数
    # ZIPアーカイブの中から特定のファイル（filename）をバイナリモードで開く
    with zf.open(filename) as f:
        # pandasでTSV（タブ区切り）として読み込み
        # quoting=3は、データ内のダブルクォート(")などを特殊文字として扱わずそのまま読み込む設定
        df = pd.read_csv(f, sep='\t', quoting=3)
    
    data = []
    # DataFrameの'sentence'列（テキスト）と'label'列（0or1）をペア
    for text, label in zip(df['sentence'], df['label']):
        
        # 2. テキストのクリーニングとID変換
        # re.subで英数字と空白以外の記号を空白に置換
        # .split()で空白区切りのリストにし、w2v（語彙辞書）にある単語のみIDに変換
        # 辞書にない単語（未知語）はこの内包表記のif文によって自動的に無視
        ids = [w2v[tk] for tk in re.sub(r'[^a-zA-Z0-9\s]', ' ', text).split() if tk in w2v]
        
        # 3. 空の事例の削除とテンソル化
        # idsが空でない（有効なトークンが1つ以上ある）場合のみリストに追加
        if ids:
            data.append({
                'text': text,                            # 元のテキスト
                'label': torch.tensor([float(label)]),   # 極性ラベルをテンソル(float型)に変換
                'input_ids': torch.tensor(ids)           # ID列をテンソル(long型)に変換
            })
    return data

# 4. ZIPファイルを開いて実行
with zipfile.ZipFile('SST-2.zip', 'r') as zf:
    # 訓練データ(train)と開発データ(dev)をそれぞれ処理
    train_data = load_sst2(zf, 'SST-2/train.tsv')
    dev_data = load_sst2(zf, 'SST-2/dev.tsv')

# 5. 結果の表示
# 最終的なデータ件数と、最初の1件のデータ構造（辞書）を表示
print(f"Train: {len(train_data)}, Dev: {len(dev_data)}")
print(f"Sample: {train_data[0]}")
