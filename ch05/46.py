import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

# お題を設定
THEME = "クリスマス" 
MODEL_NAME = 'gemini-2.5-flash'
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY") 

def build_senryu_prompt(theme):
    
    prompt = f"""
以下のテーマに基づき、日本語の川柳（五・七・五の定型詩）を10個作成してください。
詩的な表現やユーモアを含めてください。
回答は、各川柳の本文のみを、改行で区切って出力してください。他の説明や番号は一切含めないでください。

テーマ: {theme}
"""
    return prompt

def generate_senryu_list(client, theme):
    
    prompt = build_senryu_prompt(theme)
    
    try:
        # API呼び出し
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=prompt,
            config={'temperature': 0.8} # 創造性を高めるため温度を0.8にした
        )
        
        # モデルの解答を改行で分割し、リスト化
        senryu_list = [s.strip() for s in response.text.strip().split('\n') if s.strip()]
        
        return senryu_list
        
    except APIError as e:
        print(f"❌ APIエラーが発生しました: {e}")
        return None
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")
        return None


# --- メイン処理 ---
if __name__ == "__main__":
    print(f"--- 💡 お題: 『{THEME}』で川柳を生成します ---")
    
    if not API_KEY:
        print("エラー: 環境変数 'GEMINI_API_KEY' が設定されていません。")
    else:
        try:
            client = genai.Client(api_key=API_KEY)
            
            senryu_result = generate_senryu_list(client, THEME)
            
            if senryu_result:
                print("\n## 生成された川柳 10選")
                print("---")
                # 番号を振って出力
                for i, senryu in enumerate(senryu_result[:10], 1):
                    print(f"{i}. {senryu}")
                print("---")
                
                if len(senryu_result) < 10:
                    print(f"⚠️ 注意: {len(senryu_result)}個の川柳しか生成されませんでした。")
                    
        except Exception as e:
            print(f"メイン処理中にエラーが発生しました: {e}")
