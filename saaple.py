import pandas as pd
import streamlit as st
import plotly.express as px

# 데이터 로드 함수
@st.cache
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/Sobang419/news_visualization/main/sample_2.csv')

df = load_data()

# Streamlit 앱 구성
st.title("뉴스 카테고리 및 감정 분포")

# 사용자 입력 받기
selected_date = st.selectbox("날짜 선택", df['datetime'].unique())
unique_stock_codes = df['stock_code'].drop_duplicates().sort_values()
selected_stock_code = st.selectbox("주식 코드 선택", unique_stock_codes)

# 필터링된 데이터
filtered_data = df[(df['datetime'] == selected_date) & (df['stock_code'] == selected_stock_code)]

# 뉴스가 없는 경우 처리
if filtered_data.empty:
    st.error("This stock didn't have news on this day.")
else:
    # 카테고리별 감정 레이블링 분포 계산
    category_sentiment_distribution = filtered_data.groupby(['aspect', 'sentiment']).size().reset_index(name='counts')

    # Plotly Express를 사용하여 누적 막대 그래프 그리기
    fig = px.bar(category_sentiment_distribution, x='aspect', y='counts', color='sentiment', 
                 title='News Sentiment Distribution by Category',
                 labels={'counts':'Number of News Items', 'aspect':'Category', 'sentiment':'Sentiment'},
                 color_discrete_map={'Positive':'blue', 'Neutral':'grey', 'Negative':'red'})

    st.plotly_chart(fig)
