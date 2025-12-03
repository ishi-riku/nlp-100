import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# 1. 環境変数をロード
load_dotenv() 

# 2. APIキーを環境変数から安全に取得
api_key = os.getenv("GEMINI_API_KEY") 

# 3. 問題文
problem = """
9世紀に活躍した人物に関係するできごとについて述べた次のア～ウを年代の古い順に正しく並べよ。

ア　藤原時平は，策謀を用いて菅原道真を政界から追放した。
イ　嵯峨天皇は，藤原冬嗣らを蔵人頭に任命した。
ウ　藤原良房は，承和の変後，藤原氏の中での北家の優位を確立した。
"""

# 4. Zero-shot推論
prompt = f"""
以下の歴史問題に解答してください。解答はできごとの記号（ア、イ、ウ）のみを年代の古い順に「記号 → 記号 → 記号」の形式で出力してください。

--- 問題 ---
{problem}
---
"""

if api_key:
    try:
        # 5. クライアントの初期化
        client = genai.Client(api_key=api_key)

        print("--- 問題 ---")
        print(problem.strip())
        print("\nGemini APIを呼び出し中 (Zero-shot推論)...")

        # 6. モデルの呼び出し
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=prompt,
        )

        # 7. 結果の表示
        print("\n--- 解答 ---")
        print(response.text.strip())
        print("----------")
        
    except APIError as e:
        print(f"API呼び出しエラーが発生しました: {e}")
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
else:
    print("エラー: GEMINI_API_KEYが設定されていません。'.env'ファイルを確認してください。")
