import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

# 데이터 로드 함수
@st.cache
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/Sobang419/news_visualization/main/sample2.csv')

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

    # seaborn을 사용하여 누적 막대 그래프 그리기
    plt.figure(figsize=(10, 6))
    sns.barplot(x='aspect', y='counts', hue='sentiment', data=category_sentiment_distribution, palette=['blue', 'grey', 'red'])

    plt.xlabel('Category')
    plt.ylabel('Number of News Items')
    plt.title('News Sentiment Distribution by Category')
    plt.xticks(rotation=45)
    plt.legend(title='Sentiment')

    st.pyplot()
