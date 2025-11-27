import streamlit as st
import pandas as pd
import plotly.express as px
import random
import time

# 페이지 기본 설정
st.set_page_config(
    page_title="행운의 룰렛",
    page_icon="🎡",
    layout="centered"
)

# 제목 및 설명
st.title("🎡 행운의 룰렛 돌리기")
st.markdown("입력창에 후보들을 넣고 **'돌리기'** 버튼을 눌러주세요!")

# 1. 사이드바 또는 메인 화면에서 데이터 입력 받기
st.subheader("1. 후보 입력")
default_items = "짜장면\n짬뽕\n탕수육\n볶음밥\n돈까스"
items_input = st.text_area(
    "줄바꿈(Enter)으로 항목을 구분해주세요.",
    value=default_items,
    height=150
)

# 입력된 텍스트를 리스트로 변환
items = [item.strip() for item in items_input.split('\n') if item.strip()]

if items:
    # 2. 룰렛 시각화 (Plotly Pie Chart 사용)
    st.subheader("2. 룰렛 미리보기")
    
    # 데이터프레임 생성 (모든 항목의 크기를 1로 설정하여 균등하게 분할)
    df = pd.DataFrame({
        '항목': items,
        '비중': [1] * len(items)
    })
    
    # 파이 차트 그리기
    fig = px.pie(df, values='비중', names='항목', title='행운의 룰렛')
    fig.update_traces(textinfo='label+percent', textposition='inside')
    fig.update_layout(showlegend=False)
    
    st.plotly_chart(fig, use_container_width=True)

    # 3. 돌리기 버튼 및 결과 출력
    if st.button("룰렛 돌리기! 🎲", type="primary"):
        with st.spinner('두구두구두구... 룰렛이 돌아갑니다! 🎡'):
            time.sleep(2)  # 긴장감을 위한 2초 대기
        
        # 랜덤 선택
        winner = random.choice(items)
        
        st.balloons()  # 풍선 효과
        st.success(f"🎉 축하합니다! 당첨 결과는 **[{winner}]** 입니다! 🎉")
        st.snow()      # 눈 내리는 효과 (추가 축하)

else:
    st.warning("룰렛에 넣을 내용을 입력해주세요.")
