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
selected_date = st.selectbox("날짜 선택", ['날짜를 선택하세요'] + sorted(df['datetime'].unique()))

# 선택된 날짜에 대한 주식 코드만 필터링
if selected_date != '날짜를 선택하세요':
    available_stock_codes = df[df['datetime'] == selected_date]['stock_code'].unique()
else:
    available_stock_codes = df['stock_code'].unique()

# 주식 코드 선택
selected_stock_code = st.selectbox("주식 코드 선택", ['주식 코드를 선택하세요'] + sorted(available_stock_codes))

# 주식 코드와 날짜가 모두 선택된 경우에만 데이터 필터링
if selected_date != '날짜를 선택하세요' and selected_stock_code != '주식 코드를 선택하세요':
    filtered_data = df[(df['datetime'] == selected_date) & (df['stock_code'] == selected_stock_code)]
    
    # 필터링된 데이터가 있는지 확인 후 처리
    if not filtered_data.empty:
        # 카테고리별 감정 레이블링 분포 계산
        category_sentiment_distribution = filtered_data.groupby(['aspect', 'sentiment']).size().reset_index(name='counts')

        # Plotly Express를 사용하여 누적 막대 그래프 그리기
        fig = px.bar(category_sentiment_distribution, x='aspect', y='counts', color='sentiment', 
                     title='News Sentiment Distribution by Category',
                     labels={'counts':'Number of News Items', 'aspect':'Category', 'sentiment':'Sentiment'},
                     color_discrete_map={'Bullish':'red', 'Bearish':'blue', 'Neutral':'grey'},
                     text='counts')  # 막대에 개수를 표시

        # 막대 위에 값 표시를 위한 설정
        fig.update_traces(texttemplate='%{text}', textposition='outside')
        
        st.plotly_chart(fig)
    else:
        st.error("선택한 날짜에 해당하는 뉴스가 없습니다.")
else:
    st.warning("날짜와 주식 코드를 선택해 주세요.")
