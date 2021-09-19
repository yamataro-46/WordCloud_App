import streamlit as st
import matplotlib.pyplot as plt
from tweet_wordcloud import get_tweet, word_cloud


#webアプリ
st.title('トレンドミエールアプリ')
''
'①調べたいワードを検索'
'②そのワードが含まれるツイートを100件取得'
'③頻出度が高い名詞を中心に可視化'
keyWord = st.text_input('検索ワード')
cap = 'キーワード：'+ keyWord

if keyWord != '':
    wordcloud = word_cloud(get_tweet(keyWord))
    plt.imshow(wordcloud)
    plt.axis("off")
    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.pyplot()