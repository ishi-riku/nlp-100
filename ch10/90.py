import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch.nn.functional as F

def get_next_token_probs(text, model_name="gpt2"):
    # 1. モデルとトークナイザーを読み込む
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    # 2. テキストをIDの並びに変換（PyTorchテンソル形式）
    # inputs['input_ids'] は [[464, 3807, 373, 2444, 286]] のような形状になる
    inputs = tokenizer(text, return_tensors="pt")
    input_ids = inputs["input_ids"][0]

    # 入力がどう分解されたか表示
    print(f"Tokens: {[tokenizer.decode([tid]) for tid in input_ids]}\n")

    # 3. モデルに入力して各単語の「出現しやすさ」を計算
    with torch.no_grad():
        outputs = model(**inputs)
        # outputs.logits の形状は [1, 入力トークン数, 全語彙数]
        # 最後のトークン（末尾）に対応する語彙全体のスコアを取り出す
        last_token_logits = outputs.logits[0, -1, :]

        # 4. スコアをSoftmax関数で「合計が100%になる確率」に変換
        # $P(x_i) = \frac{e^{x_i}}{\sum e^{x_j}}$
        probs = F.softmax(last_token_logits, dim=-1)

    # 5. 確率の高い上位10個を取得
    top_probs, top_ids = torch.topk(probs, k=10)

    # 結果表示
    for i, (pr, idx) in enumerate(zip(top_probs, top_ids)):
        token_str = tokenizer.decode([idx])
        print(f"{i+1}: '{token_str}' ({pr:.2%})")

if __name__ == "__main__":
    get_next_token_probs("The movie was full of")
