import time
import streamlit as st
import openai
import os
apikey = os.environ['API_KEY']
openai.api_key = apikey

st.title('イチング占い')

def render()->st:
    bg_img = '''
    <style>
    .stApp {
      background-image: url("");
      background-size: cover;
      background-repeat: no-repeat;
    }
    </style>
    '''

    return st.markdown(bg_img, unsafe_allow_html=True)
render()

st.write("<span style='color: purple; font-size: 16px;'>イチングは、古代中国の占いや哲学に関する古典で、紀元前1000年頃に成立したとされています。\
もともとは自然現象を観察し、それらの変化を記録するためのものでしたが、後に占いや哲学的な思考の道具として発展しました。\
イチングは、六十四の卦（八卦を組み合わせたもの）で構成されており、それぞれの卦には独自の意味があります。\
イチングの占いは、「爻（やお）」と呼ばれる六つの線の組み合わせで行われます。\
爻には陰（破線）と陽（実線）の2種類があり、それぞれの組み合わせによって卦が決まります。\
質問者が持っている問題や状況を考慮し、卦の解釈を通してアドバイスや洞察を得ることができます。\
イチングは、単なる占いの道具としてだけでなく、道教や儒教、仏教などの哲学的思想とも密接に関連しています。\
それゆえ、イチングは自己啓発や人生の指針を求めるために利用されることもあります。\
また、その象徴的な言語や抽象的な概念が、現代の心理学や哲学にも影響を与えています。\
イチングに関心がある場合は、易経のテキストを読んでみたり、占いの方法を学んでみたりすることがおすすめです。\
イチングは、自分自身や他者との関係性をより深く理解する手段として、\
また人生における様々な局面に対処するための知恵を学ぶ方法として、多くの人にとって有益であると言われています。</span>",unsafe_allow_html=True)


#<span style="color: blue; font-size: 16px;">Hello, world!</span>
#, unsafe_allow_html=True


#OpenAI APIキーを設定する関数
def setup_openai_api():
    openai.api_key = apikey


# ユーザーの入力を取得する関数
def get_user_input() -> str:
    """
    Streamlitのtext_areaウィジェットで、ユーザーからの入力を取得する。
    """
    return st.text_area("データ", value="本名：\n 生年月日：")


# OpenAIに問い合わせを送信し、応答を取得する関数
def generate_response(system_text: str, user_text: str) -> openai.api_resources.Completion:
    """
    OpenAIのChatCompletion APIを使って、ユーザーの入力に応答する。
    Args:
        system_text (str): システムの名前（例：アシスタントAI）
        user_text (str): ユーザーの入力

    Returns:
        openai.api_resources.Completion: OpenAIから返された応答
    """
    message = [{"role": "system", "content": system_text}, {"role": "user", "content": user_text}]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=message,
        max_tokens=3000,
        temperature=0.7,
        stream=True
    )
    return response


# OpenAIから受け取った応答を表示する関数
def display_response(response: openai.api_resources.Completion):
    """
    OpenAIから受け取った応答をStreamlitのウィジェット上に表示する。
    Args:
        response (openai.api_resources.Completion): OpenAIから返された応答
    """
    partial_words = ""
    answer = st.empty()
    for chunk in response:
        if chunk and "delta" in chunk["choices"][0] and "content" in chunk["choices"][0]["delta"]:
            partial_words += chunk["choices"][0]["delta"]["content"]
            answer.write(partial_words)


# アプリケーションのメイン関数
def main():
    setup_openai_api()  # OpenAI APIキーを設定する

    system_text = "あなたは有能なイチング占い師です。\
        入力されたデータからRANDを生成し明示、記録用のテーブル表も用意してください。\
        RANDコインを仮想空間上に3枚用意し、3枚同時に６回振って、3枚が表か裏かをそれぞれテーブルに記録してゆく。\
        表表表は陽爻、表裏表は隠爻というふうにテーブル表に明示。\
        全ての結果をイチングの表を参考に照合し、64卦のどれかに決まったかを明示してください。\
        64卦のどれかになるまで繰り返してください。\
        次に決まった卦の漢文を明示する。古事があればそれも簡単に明記してください。\
        その次に日本語でわかりやすく現代の風習に沿って1,過去の自分。2,現在の自分。3,今後の自分、のように具体例とエピソードを交えながら提示\
        最後に「金運」を総合的に書く\
    "
    user_text = get_user_input()  # ユーザーの入力を取得する
    is_generate_clicked = st.button("占う！")

    if is_generate_clicked:
        response = generate_response(system_text, user_text)  # OpenAIに問い合わせを送信し、応答を取得する
        display_response(response)  # OpenAIから受け取った応答を表示する


if __name__ == "__main__":
    main()
    
    