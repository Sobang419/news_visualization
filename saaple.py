import pandas as pd
import streamlit as st
import altair as alt

# 데이터 로드 함수
@st.cache
def load_data():
    return pd.read_csv('https://raw.githubusercontent.com/Sobang419/news_visualization/main/sample_2.csv')

df = load_data()

# Streamlit 앱 구성
st.title("뉴스 카테고리 및 감정 분포")

# 사용자 입력 받기
selected_date = st.selectbox("날짜 선택", df['datetime'].unique())

# 주식 코드 입력 또는 선택
input_stock_code = st.text_input("주식 코드 입력")
selected_stock_code = st.selectbox("주식 코드 선택", df['stock_code'].unique(), format_func=lambda x: '입력값 사용' if x == input_stock_code else x)

# 주식 코드 검증
if input_stock_code and input_stock_code not in df['stock_code'].unique():
    st.error("wrong stock_code")
else:
    selected_stock_code = selected_stock_code or input_stock_code

    # 필터링된 데이터
    filtered_data = df[(df['datetime'] == selected_date) & (df['stock_code'] == selected_stock_code)]

    # 뉴스가 없는 경우 처리
    if filtered_data.empty:
        st.error("This stock didn't have news on this day.")
    else:
        # 카테고리별 감정 레이블링 분포 계산
        category_sentiment_distribution = filtered_data.groupby(['datetime', 'aspect', 'sentiment']).size().reset_index(name='counts')

        # 누적 막대 차트 그리기
        chart = alt.Chart(category_sentiment_distribution).mark_bar().encode(
            x=alt.X('datetime:N', title='Date'),
            y=alt.Y('counts:Q', title='Number of News Items', stack='normalize'),
            color=alt.Color('sentiment:N', scale=alt.Scale(domain=['Positive', 'Neutral', 'Negative'], range=['blue', 'grey', 'red'])),
            column=alt.Column('aspect:N', title='Category')
        )

        st.altair_chart(chart, use_container_width=True)
