import os
import csv
from dotenv import load_dotenv
from google import genai

TEST_FILE = "professional_medicine.csv"
MODEL_NAME = 'gemini-2.5-flash'
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# 1.データ読み込み関数
def load_csv_data(filepath):
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) == 6:
                data.append({
                    'question': row[0],
                    'choices': [row[1], row[2], row[3], row[4]],
                    'correct_symbol': row[5].strip().upper()
                })
    return data

# 2.プロンプト生成関数
def build_prompt(record):
    symbols = ['A', 'B', 'C', 'D']
    choices_text = "\n".join(
        f"選択肢{symbols[i]}: {record['choices'][i]}" for i in range(4)
    )

    prompt = f"""
以下の四択問題に解答してください。
解答は、問題文と選択肢の内容を考慮し、正解となる選択肢の記号のみ（A, B, C, D）を出力してください。記号以外の文字（説明、
記号名、句読点など）は一切含めないでください。

--- 問題 ---
問題文: {record['question']}
{choices_text}
解答記号:
"""
    return prompt

# 3.評価実行関数
def evaluate_jmmlu(client, test_data):
    correct_count = 0
    total_count = len(test_data)

    print(f"--- 評価開始 (全 {total_count} 問) ---")

    for i, record in enumerate(test_data):
        correct_symbol = record['correct_symbol']
        prompt = build_prompt(record)

        # API呼び出し
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config={'temperature': 0.8}
        )

        # モデルの解答を整形
        model_answer_symbol = response.text.strip().split()[0].upper()

        # 判定
        is_correct = (model_answer_symbol == correct_symbol)
        if is_correct:
            correct_count += 1

        print(f"問 {i+1}: 正解={correct_symbol}, モデル解答={model_answer_symbol}, 結果={'⭕' if is_correct else '❌'}")

    # 4.結果出力
    accuracy = (correct_count / total_count) * 100
    print("\n--- 評価結果 ---")
    print(f"正解数: {correct_count} 問")
    print(f"正解率: {accuracy:.2f}%")
    print("----------------")


# --- メイン処理 ---
if __name__ == "__main__":
    if not API_KEY:
        print("エラー: GEMINI_API_KEYが設定されていません。")
    else:
        try:
            client = genai.Client(api_key=API_KEY)
            test_data = load_csv_data(TEST_FILE)
            evaluate_jmmlu(client, test_data)
        except Exception as e:
            # 簡略化のため、ファイルが見つからないなどのエラーはここでまとめて表示
            print(f"処理中にエラーが発生しました: {e}")
