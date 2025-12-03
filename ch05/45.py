import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

MODEL_NAME = 'gemini-2.5-flash'
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY") 

def solve_station_problem(): 
    # プロンプト
    prompt = """
直前の会話を参考に以下の問題に解答してください。
回答は、最終的な駅数のみを数字で出力してください。余計な説明は一切含めないでください。

--- 直前の会話 ---
つばめちゃんは渋谷駅から東急東横線に乗り、自由が丘駅で乗り換えました。東急大井町線の大井町方面の電車に乗り換えたとき、各駅停車に乗車すべきところ、間違えて急行に乗車してしまったことに気付きました。自由が丘の次の急行停車駅で降車し、反対方向の電車で一駅戻った駅がつばめちゃんの目的地でした。目的地の駅の名前を答えてください。
→目的地は緑が丘駅

--- 問題 ---
さらに、つばめちゃんが自由が丘駅で乗り換えたとき、先ほどとは反対方向の急行電車に間違って乗車してしまった場合を考えます。目的地の駅に向かうため、自由が丘の次の急行停車駅で降車した後、反対方向の各駅停車に乗車した場合、何駅先の駅で降りれば良いでしょうか？
"""
    
    if not API_KEY:
        print("エラー: 環境変数 'GEMINI_API_KEY' が設定されていません。")
        return None

    try:
        client = genai.Client(api_key=API_KEY)
        
        print("GeminiAPIを呼び出し中...")
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=prompt,
            config={'temperature': 0}
        )
        
        # モデルの解答を取得し、整形
        model_answer = response.text.strip()
        
        print("-" * 30)
        print(f"回答（駅数）: {model_answer}")
        return model_answer
        
    except APIError as e:
        print(f"❌ APIエラーが発生しました: {e}")
        print("APIキーや利用制限（クォータ）を確認してください。")
        return None
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")
        return None

# --- メイン処理 ---
if __name__ == "__main__":
    solve_station_problem()
