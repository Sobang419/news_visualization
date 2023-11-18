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

# 주식 코드 직접 입력 또는 선택
input_stock_code = st.text_input("주식 코드 입력")
if input_stock_code:
    selected_stock_code = input_stock_code
else:
    selected_stock_code = st.selectbox("주식 코드 선택", df['stock_code'].unique())

# 주식 코드 검증
if selected_stock_code not in df['stock_code'].unique():
    st.error("wrong stock_code")
    # 데이터를 처리하지 않고 조기에 함수를 종료
else:
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
