import pandas as pd
import streamlit as st
import altair as alt

@st.cache
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/Sobang419/news_visualization/main/sample_2.csv')

df = load_data()

# Streamlit 앱 구성
st.title("뉴스 카테고리 및 감정 분포")

# 사용자 입력 받기
selected_date = st.selectbox("날짜 선택", df['datetime'].unique())
selected_stock_code = st.selectbox("주식 코드 선택", df['stock_code'].unique())

# 필터링된 데이터
filtered_data = df[(df['datetime'] == selected_date) & (df['stock_code'] == selected_stock_code)]

# 뉴스가 없는 경우 처리
if filtered_data.empty:
    st.error("This stock didn't have news on this day.")
else:
    # 카테고리별 감정 레이블링 분포 계산
    category_sentiment_distribution = filtered_data.groupby(['aspect', 'sentiment']).size().reset_index(name='counts')

    # 가로 막대 차트 그리기
    chart = alt.Chart(category_sentiment_distribution).mark_bar().encode(
        x=alt.X('aspect:N', title='Category', axis=alt.Axis(labelAngle=0)), # X축 레이블 가로 배치
        y=alt.Y('counts:Q', title='Number of News Items', stack='zero', scale=alt.Scale(domain=[0, 15])), # Y축 범위 설정
        color=alt.Color('sentiment:N', scale=alt.Scale(domain=['Positive', 'Neutral', 'Negative'], range=['blue', 'grey', 'red']))
    )

    st.altair_chart(chart, use_container_width=True)
