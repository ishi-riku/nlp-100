import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

MODEL_NAME = 'gemini-2.5-flash'
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY") 

# 評価対象の川柳リスト
SENRYU_LIST = [
    "1. 枕元　夢と希望と　猫の毛と",
    "2. 煙突は　マンション暮らし　無理がある",
    "3. 電球が　絡まるツリー　冬の戦",
    "4. 飾るたび　猫が狙うは　玉一つ",
    "5. 丸焼きは　年に一度の　腕自慢",
    "6. ケーキより　チキンに夢中　パパと僕",
    "7. 街の灯り　隣に君と　星の夜",
    "8. 雪降れば　ホワイトクリスマス　翌日凍る",
    "9. サンタさん　ダイエットは　年明けに",
    "10. トナカイも　渋滞知らず　空の道"
]

def build_evaluation_prompt(senryu_list):
    
    senryu_text = "\n".join(senryu_list)
    
    prompt = f"""
あなたは大規模言語モデルの審査員です。
以下の10個の川柳について、その面白さを10段階で評価してください。

評価結果は、以下の形式で出力してください。

1. [点数]/10、評価理由
2. [点数]/10、評価理由
...
10. [点数]/10、評価理由

--- 評価対象の川柳 ---
{senryu_text}
"""
    return prompt

def evaluate_senryu(client, senryu_list):
    
    prompt = build_evaluation_prompt(senryu_list)
    
    try:
        # API呼び出し
        response = client.models.generate_content(
            model=MODEL_NAME, 
            contents=prompt,
            # 評価にランダム性は不要なため、温度は低めに設定
            config={'temperature': 0.2}
        )
        
        return response.text.strip()
        
    except APIError as e:
        print(f"❌ APIエラーが発生しました: {e}")
        print("APIキーや利用制限（クォータ）を確認してください。")
        return None
    except Exception as e:
        print(f"❌ 予期せぬエラーが発生しました: {e}")
        return None


# --- メイン処理 ---
if __name__ == "__main__":
    
    if not API_KEY:
        print("エラー: 環境変数 'GEMINI_API_KEY' が設定されていません。")
    else:
        try:
            client = genai.Client(api_key=API_KEY)
            
            print("Geminiを審査員として、川柳の面白さ評価を開始します...")
            
            evaluation_result = evaluate_senryu(client, SENRYU_LIST)
            
            if evaluation_result:
                print("\n## 評価結果（面白さ 10段階評価）")
                print("---")
                # 結果をそのまま出力
                print(evaluation_result)
                print("---")
                
        except Exception as e:
            print(f"メイン処理中にエラーが発生しました: {e}")
