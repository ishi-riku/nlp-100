import os
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError

MODEL_NAME = 'gemini-2.5-flash'
load_dotenv() 
API_KEY = os.getenv("GEMINI_API_KEY") 

TEXT_TO_COUNT = """
吾輩は猫である。名前はまだ無い。
どこで生れたかとんと見当がつかぬ。何でも薄暗いじめじめした所でニャーニャー泣いていた事だけは記憶している。吾輩はここで始めて人間というものを見た。しかもあとで聞くとそれは書生という人間中で一番獰悪な種族であったそうだ。この書生というのは時々我々を捕えて煮て食うという話である。しかしその当時は何という考もなかったから別段恐しいとも思わなかった。ただ彼の掌に載せられてスーと持ち上げられた時何だかフワフワした感じがあったばかりである。掌の上で少し落ちついて書生の顔を見たのがいわゆる人間というものの見始であろう。この時妙なものだと思った感じが今でも残っている。第一毛をもって装飾されべきはずの顔がつるつるしてまるで薬缶だ。その後猫にもだいぶ逢ったがこんな片輪には一度も出会わした事がない。のみならず顔の真中があまりに突起している。そうしてその穴の中から時々ぷうぷうと煙を吹く。どうも咽せぽくて実に弱った。これが人間の飲む煙草というものである事はようやくこの頃知った。
"""

def count_text_tokens(client, text):
    
    try:
        # count_tokensメソッドの呼び出し
        response = client.models.count_tokens(
            model=MODEL_NAME,
            contents=[text] # count_tokensはリストを要求するため
        )
        
        # トークン数を取得
        token_count = response.total_tokens
        
        return token_count
        
    except APIError as e:
        print(f"❌ APIエラーが発生しました: {e}")
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
            
            print("--- トークン計測開始 ---")
            print(f"テキスト長（文字数）: {len(TEXT_TO_COUNT.strip())} 文字")
            
            token_count = count_text_tokens(client, TEXT_TO_COUNT)
            
            if token_count is not None:
                print("-" * 30)
                print(f"トークン数 ({MODEL_NAME}): {token_count} トークン")
                
        except Exception as e:
            print(f"メイン処理中にエラーが発生しました: {e}")
