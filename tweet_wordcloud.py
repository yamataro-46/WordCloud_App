import tweepy
import re
import MeCab
from wordcloud import WordCloud
import streamlit as st

#検索ワードを含むツイートを100件取得
def get_tweet(key_word):
    # APIの秘密鍵
    CONSUMER_KEY = st.secrets["CONSUMER_KEY"]
    CONSUMER_SECRET = st.secrets["CONSUMER_SECRET"]
    ACCESS_TOKEN_KEY = st.secrets["ACCESS_TOKEN_KEY"]
    ACCESS_TOKEN_SECRET = st.secrets["ACCESS_TOKEN_SECRET"]

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)

    #ツイート取得
    results = api.search(q=key_word, count=100, include_rts=False)

    #不要なものの除去済みのツイート文を1つのテキスト文につなげる
    text = ''
    for result in results:

        # ハッシュタグの除去
        result.text = re.sub(r'#[^ ]+ *', '', result.text)
        
        # スクリーンネームの除去
        result.text = re.sub(r'@[\w_]+ *', '', result.text)
        
        # URLの除去
        result.text = re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+ *', '', result.text)
        
        # 絵文字などの除去
        result.text = re.sub(r'[^、。!?ー〜1-9a-zA-Zぁ-んァ-ヶ亜-腕纊-黑一-鿕]', '', result.text)

        text += result.text

    text = text.replace('RT', '')
    text = text.replace(key_word, '')

    return text

#名詞の書き込み頻度順に可視化
def word_cloud(text):
    mecab = MeCab.Tagger()
    parts = mecab.parse(text)

    #名詞のみ取り出しリストに格納
    nouns = []
    for part in parts.split('\n')[:-2]:
        if '名詞' in part.split('\t')[4]:
            nouns.append(part.split('\t')[0])

    words = ' '.join(nouns)

    font_path = 'ヒラギノ角ゴシック W4.ttc'
    wc = WordCloud(width=480, height=320, background_color='white', font_path=font_path)
    wc.generate(words)
    
    return wc
