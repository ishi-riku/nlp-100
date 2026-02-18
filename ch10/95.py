import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def run_conversation():
    # 1. モデルとトークナイザーの準備 (GPT型の TinyLlama を使用)
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16)
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # 2. 会話履歴の定義
    # 最初の問いと、すでに得られている応答をリストに格納します
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What do you call a sweet eaten after dinner?"},
        {"role": "assistant", "content": "A post-dinner treat or dessert."}
    ]
    
    # 追加の問いかけを履歴に追記
    messages.append({"role": "user", "content": "Please give me the plural form of the word with its spelling in reverse order."})

    # 3. チャットテンプレートを適用して、モデルに与える「最終的なプロンプト」を作成
    # tokenize=False にすることで、連結された生の文字列を確認できます
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    print(f"--- 言語モデルに与えられるプロンプト ---\n{prompt}\n" + "="*40)

    # 4. 応答の生成
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=False  # 確実な回答を得るため
        )

    # 5. 今回の生成部分（回答のみ）を抽出して表示
    # 入力プロンプトの長さ以降のトークンをデコードします
    input_length = inputs.input_ids.shape[1]
    response = tokenizer.decode(outputs[0][input_length:], skip_special_tokens=True)
    
    print(f"--- 追加質問に対する応答 ---\n{response}")

if __name__ == "__main__":
    run_conversation()
