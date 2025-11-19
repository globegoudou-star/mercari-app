import streamlit as st
import google.generativeai as genai
from PIL import Image

# ==========================================
# 設定：鳥山様用のプロンプト
# ==========================================
SYSTEM_PROMPT = """
あなたはプロのメルカリ物販プレイヤーです。
アップロードされた商品画像をもとに、以下のフォーマットで出品用テキストを作成してください。

## 出力ルール
1. **【タイトル】**は検索キーワードを詰め込み、40文字以内で作成。
2. **【説明文】**は以下のテンプレートを使用。
3. **発送（配送方法・日数）については一切記載しないこと。**
4. 出力はテキストのみ。余計な挨拶は不要。

## 出力フォーマット
**【タイトル】**
（商品名・型番・特徴・★記号などを含めた40文字以内のタイトル）

**【説明文】**
--------------------------------------------------
ご覧いただきありがとうございます！
その他もたくさんの良質な品物をお安く出品しております。
ぜひフォローお願いいたします！

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
st.set_page_config(page_title="メルカリ出品くん", layout="wide")

st.title("📦 メルカリ出品くん for 丸蔵")

# --- APIキーの自動取得 ---
# Secretsに保存されていればそれを使い、なければ入力欄を表示する
api_key = None
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
else:
    with st.sidebar:
        api_key = st.text_input("Google API Keyを入力", type="password")

# -----------------------

uploaded_file = st.file_uploader("商品画像をアップロード", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="対象画像", width=300)
    
    if st.button("📝 説明文を生成する", type="primary"):
        if not api_key:
            st.error("APIキーが設定されていません。")
        else:
            with st.spinner("AIが考え中..."):
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([SYSTEM_PROMPT, image])
                    st.success("生成完了！")
                    st.code(response.text, language="markdown")
                except Exception as e:
                    st.error(f"エラー: {e}")
