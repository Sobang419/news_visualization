import pandas as pd
import streamlit as st
import altair as alt
@st.cache
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/Sobang419/news_visualization/main/sample.csv')

df = load_data()

# Streamlit 앱 구성
st.title("뉴스 카테고리 및 감정 분포")

# 사용자 입력 받기
selected_date = st.selectbox("날짜 선택", df['datetime'].unique())
selected_stock_code = st.selectbox("주식 코드 선택", df['stock_code'].unique())

# 필터링된 데이터
filtered_data = df[(df['datetime'] == selected_date) & (df['stock_code'] == selected_stock_code)]

# 카테고리별 감정 레이블링 분포 계산
category_sentiment_distribution = filtered_data.groupby('aspect')['sentiment'].value_counts().unstack().fillna(0)

# 가로 막대 그래프 그리기
chart = alt.Chart(category_sentiment_distribution.reset_index()).mark_bar().encode(
    x=alt.X('aspect:N', title='Category'),
    y=alt.Y('sum(sentiment):Q', title='Number of News Items'),
    color='aspect:N'
)

st.altair_chart(chart, use_container_width=True)
