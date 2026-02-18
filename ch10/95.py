import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

def run_qwen_session():
    # 1. モデル
    model_id = "Qwen/Qwen2.5-3B-Instruct"
    
    print("モデルを読み込んでいます。")
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16, 
        device_map="auto"
    )

    # 2. 設定
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What do you call a sweet eaten after dinner?"},
        {"role": "assistant", "content": "A post-dinner treat or dessert."}
    ]
    
    # 追加質問
    messages.append({
        "role": "user", 
        "content": "Please give me the plural form of the word with its spelling in reverse order."
    })

    # 3. プロンプト構築
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    
    # 4. 生成実行
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        outputs = model.generate(
            **inputs, 
            max_new_tokens=100,
            do_sample=False # 最も確率が高い答え（Greedy）
        )

    # 5. 結果の表示
    response = tokenizer.decode(outputs[0][inputs.input_ids.shape[1]:], skip_special_tokens=True)
    print("\n" + "="*40)
    print(f"--- Qwen2.5-3B の応答 ---\n{response}")
    print("="*40)

if __name__ == "__main__":
    run_qwen_session()
