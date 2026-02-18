import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def eval_ppl(sentences):
    # モデルとトークナイザーをロード
    model_name = "gpt2"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    for text in sentences:
        # 1. テキストをトークンIDに変換
        inputs = tokenizer(text, return_tensors="pt")
        input_ids = inputs["input_ids"]

        # 2. モデルを実行。labelsを入力と同じに設定することでLoss（交差エントロピー）が自動計算される
        # labelsを指定すると、次のトークンを当てるタスクとして計算される
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
            loss = outputs.loss

        # 3. PPL = exp(平均Loss) で算出
        # モデルが次の単語をどれくらい絞り込めているか（平均的な選択肢数）を示す
        ppl = torch.exp(loss).item()
        print(f"PPL: {ppl:6.2f} | 文: {text}")

if __name__ == "__main__":
    # 文法的に正しいペアと誤ったペア
    lines = [
        "The movie was full of surprises",
        "The movies were full of surprises",
        "The movie were full of surprises",
        "The movies was full of surprises"
    ]
    eval_ppl(lines)
