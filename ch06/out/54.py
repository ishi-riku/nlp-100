import gensim
import re
import os

# 1. 設定
MODEL_PATH = 'GoogleNews-vectors-negative300.bin.gz' 
INPUT_FILE = 'questions-words.txt'

# 2. Word2Vecモデルのロード
try:
    print(f"Word2Vecモデル ({MODEL_PATH}) をロード中")
    # load_word2vec_formatを使用。バイナリ形式なのでbinary=True
    model = gensim.models.KeyedVectors.load_word2vec_format(
        MODEL_PATH, binary=True
    )
    print("ロード完了。")
except FileNotFoundError:
    print(f"エラー: モデルファイルが見つかりません。: {MODEL_PATH}")
    print("実行を中断します。")
    exit()
except Exception as e:
    print(f"モデルのロード中にエラーが発生しました: {e}")
    print("実行を中断します。")
    exit()

# 3. データの抽出と処理

def solve_word_analogy(input_file, model):
    """
    指定されたファイルから: capital-common-countriesセクションを抽出し、
    類推タスクを実行します。
    """
    results = []
    in_target_section = False
    target_section = ": capital-common-countries"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                
                # セクションヘッダーの処理
                if line.startswith(':'):
                    if line == target_section:
                        in_target_section = True
                        print(f"\n--- {target_section} の処理を開始します ---")
                        continue
                    elif in_target_section:
                        # 目的のセクションが終了
                        in_target_section = False
                        break
                    else:
                        continue
                
                # 目的のセクション内のデータ処理
                if in_target_section:
                    # 4つの単語 (首都1, 国1, 首都2, 国2) を抽出
                    words = line.split() 
                    if len(words) == 4:
                        # 類推の計算: vec(国2) - vec(国1) + vec(首都1) = 求める首都
                        # ファイルのデータ形式: [首都1] [国1] [首都2] [国2]
                        # 求める式: vec(words[3]) - vec(words[1]) + vec(words[0])
                        
                        # 国2 (words[3]) と 首都1 (words[0]) を positive
                        # 国1 (words[1]) を negative
                        positive_words = [words[3], words[0]] 
                        negative_words = [words[1]]            
                        
                        # 目的の単語 (首都2: words[2]) を排除リストに追加
                        # これがないと、多くの場合、答えであるwords[2]自体がトップに来てしまいます。
                        # 正確な評価のためには、類推タスクの答えとなる単語も排除すべきですが、
                        # 今回はシンプルな実装として、最も類似度の高い単語をそのまま取得します。
                        
                        try:
                            # most_similarで類似度を計算 (topn=1)
                            similar_words = model.most_similar(
                                positive=positive_words, 
                                negative=negative_words, 
                                topn=1
                            )
                            
                            # 結果を格納
                            if similar_words:
                                result_word, similarity = similar_words[0]
                                results.append(
                                    f"事例: {words[0]} ({words[1]}) -> {words[2]} ({words[3]}) | "
                                    f"予測単語: {result_word} (類似度: {similarity:.4f}) | "
                                    f"（期待される単語: {words[2]}）"
                                )
                            else:
                                results.append(f"事例: {words[0]} {words[1]} -> {words[2]} {words[3]} | 予測単語: 見つかりませんでした")
                                
                        except KeyError as e:
                            # モデルに単語が存在しない場合
                            # e の内容は通常、引用符で囲まれた単語
                            missing_word = str(e).strip("'")
                            results.append(
                                f"事例: {words[0]} {words[1]} -> {words[2]} {words[3]} | "
                                f"エラー: モデルに単語 '{missing_word}' が見つかりません"
                            )
                        except Exception as e:
                            results.append(f"事例: {words[0]} {words[1]} -> {words[2]} {words[3]} | 予測中にエラーが発生: {e}")

    except FileNotFoundError:
        print(f"\nエラー: 入力ファイルが見つかりません。: {input_file}")
        return []
    except Exception as e:
        print(f"\nファイルの読み込み中にエラーが発生しました: {e}")
        return []
        
    return results

# 4. 実行と結果の出力
analogy_results = solve_word_analogy(INPUT_FILE, model)

print("\n--- 類推結果 ---")
if analogy_results:
    for res in analogy_results:
        print(res)
else:
    print("結果がありませんでした。ファイルの内容またはパスを確認してください。")
