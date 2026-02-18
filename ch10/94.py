import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def run_chat_session():
    # 1. モデルの準備 (GPT型のオープンモデル TinyLlama を使用)
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto")

    # 2. 設定 (この辞書形式が入力になる)
    messages = [
        {"role": "system", "content": "You are a concise assistant."},
        {"role": "user", "content": "What do you call a sweet eaten after dinner?"}
    ]

    # 3. チャットテンプレートの適用
    # tokenize=False で、モデルに送られる直前の生の文字列を確認できる
    # add_generation_prompt=True で「Assistant: 」という返信の合図を末尾に追加する
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    print(f"--- モデルに渡されるプロンプト ---\n{prompt}\n")

    # 4. 生成実行 (プロンプトをID化してモデルに入力)
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=20,   # 20トークン
            do_sample=False      # 最も確率の高い回答を固定で出す(Greedy Search)
        )

    # 5. 結果の表示 (回答だけを表示)
    full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    response = full_output.split("assistant\n")[-1].strip()
    
    print(f"--- モデルの応答 ---\n{response}")

if __name__ == "__main__":
    run_chat_session()
