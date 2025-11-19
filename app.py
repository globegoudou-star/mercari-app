import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 設定：鳥山様用のプロンプト（指示書）
# ==========================================
SYSTEM_PROMPT = """
あなたはプロのメルカリ物販プレイヤーです。
アップロードされた商品画像をもとに、以下のフォーマットで出品用テキストを作成してください。

## 出力ルール
1. **【タイトル】**は検索キーワードを詰め込み、40文字以内で作成。
2. **【説明文】**は以下のテンプレートを使用。
3. **発送（配送方法・日数）については一切記載しないこと。**（これは絶対ルールです）
4. 出力はテキストのみ。余計な挨拶は不要。

## 出力フォーマット
**【タイトル】**
（商品名・型番・特徴・★記号などを含めた40文字以内のタイトル）

**【説明文】**
--------------------------------------------------
ご覧いただきありがとうございます！
その他もたくさん良質な品物をお安く出品しております！
フォロー宜しくお願い致します！

■商品情報
・商品名：
・ブランド/メーカー：
・状態：（画像から推測）
・サイズ/スペック：（画像から読み取れる場合のみ）

■特記事項
中古品のため、多少の使用感はご了承ください。
簡易清掃・消毒済みです。

#（関連タグ5〜10個）
--------------------------------------------------

**【設定価格の目安】**
・強気価格： ¥
・即売れ価格： ¥
"""

# ==========================================
# アプリの画面構成
# ==========================================
st.set_page_config(page_title="メルカリ出品くん for 丸蔵", layout="wide")

st.title("📦 メルカリ出品くん for 丸蔵")
st.markdown("写真をアップロードすると、AIがタイトルと説明文を自動作成します。")

# サイドバー：APIキー入力
with st.sidebar:
    st.header("設定")
    api_key = st.text_input("Google API Keyを入力", type="password")
    st.markdown("[APIキーの取得はこちら](https://aistudio.google.com/app/apikey)")

# メインエリア：画像アップロード
uploaded_file = st.file_uploader("商品画像をここにドラッグ＆ドロップ", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None and api_key:
    # 画像を表示
    image = Image.open(uploaded_file)
    st.image(image, caption="アップロードされた画像", width=300)
    
    # ボタンが押されたらAIを作動
    if st.button("📝 説明文を生成する", type="primary"):
        with st.spinner("AIが画像を解析中...少々お待ちください"):
            try:
                # Geminiの設定
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # AIに画像と指示を渡す
                response = model.generate_content([SYSTEM_PROMPT, image])
                
                # 結果の表示
                st.success("生成完了！")
                st.markdown("### ▼ 生成されたテキスト（コピーして使用）")
                st.code(response.text, language="markdown")
                
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")

elif uploaded_file is not None and not api_key:
    st.warning("👈 左のサイドバーにAPIキーを入力してください")