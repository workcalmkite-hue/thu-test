import streamlit as st
import streamlit.components.v1 as components
import random

# 페이지 설정
st.set_page_config(page_title="리얼 룰렛", page_icon="🎡")

st.title("🎡 리얼하게 돌아가는 룰렛")

# 1. 사이드바에서 데이터 입력
st.sidebar.header("메뉴 입력")
default_items = "짜장면\n짬뽕\n탕수육\n볶음밥\n마라탕"
items_input = st.sidebar.text_area("항목을 줄바꿈으로 입력하세요", value=default_items, height=150)
items = [item.strip() for item in items_input.split('\n') if item.strip()]

# 색상 팔레트 (룰렛 조각 색상)
colors = ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF", "#FF9F40", "#8AC926", "#1982C4", "#6A4C93"]

if not items:
    st.error("항목을 하나 이상 입력해주세요!")
    st.stop()

# 2. 당첨자 선정 로직 (버튼 클릭 시)
# 세션 상태를 사용하여 룰렛이 돌아가는 동안 값이 바뀌지 않게 함
if 'target_index' not in st.session_state:
    st.session_state.target_index = 0
if 'is_spinning' not in st.session_state:
    st.session_state.is_spinning = False

col1, col2 = st.columns([1, 2])

with col1:
    if st.button("🎰 룰렛 돌리기!", type="primary", use_container_width=True):
        st.session_state.target_index = random.randint(0, len(items) - 1)
        st.session_state.is_spinning = True

# 3. HTML/JS 룰렛 생성 함수
def get_roulette_html(items, target_index, is_spinning):
    # 아이템을 JS 배열 문자열로 변환
    items_js = str(items)
    colors_js = str((colors * 5)[:len(items)]) # 색상이 부족하면 반복
    
    # 회전 각도 계산
    # 기본 5바퀴(1800도) + 당첨 위치 계산
    # 캔버스는 0도가 3시 방향이므로 보정 필요.
    if is_spinning:
        # 각 조각의 각도
        slice_deg = 360 / len(items)
        # 목표 지점이 12시 방향(270도 위치)에 오도록 계산
        # target_index가 가리키는 조각의 중심이 화살표에 오게 하려면:
        stop_deg = 360 - (target_index * slice_deg) 
        # 랜덤 오차범위 제거하고 정확히 가운데 멈추게 설정
        rotation = 1800 + stop_deg 
    else:
        rotation = 0

    return f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div style="position: relative; width: 400px; height: 400px;">
            <div style="
                position: absolute;
                top: -15px;
                left: 50%;
                transform: translateX(-50%);
                width: 0; 
                height: 0; 
                border-left: 15px solid transparent;
                border-right: 15px solid transparent;
                border-top: 30px solid #FF0000;
                z-index: 10;
            "></div>
            
            <canvas id="wheel" width="400" height="400" style="
                transition: transform 4s cubic-bezier(0.25, 0.1, 0.25, 1);
                transform: rotate({rotation}deg);
            "></canvas>
        </div>
        <h2 id="result" style="margin-top: 20px; color: #333; height: 30px;"></h2>
    </div>

    <script>
        const canvas = document.getElementById('wheel');
        const ctx = canvas.getContext('2d');
        const items = {items_js};
        const colors = {colors_js};
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = width / 2;
        
        const sliceAngle = (2 * Math.PI) / items.length;

        // 룰렛 그리기
        startAngle = -Math.PI / 2; // 12시 방향부터 그리기 시작 (보정)

        for (let i = 0; i < items.length; i++) {{
            ctx.beginPath();
            ctx.moveTo(centerX, centerY);
            ctx.arc(centerX, centerY, radius, startAngle, startAngle + sliceAngle);
            ctx.fillStyle = colors[i];
            ctx.fill();
            ctx.stroke();
            
            // 텍스트 그리기
            ctx.save();
            ctx.translate(centerX, centerY);
            ctx.rotate(startAngle + sliceAngle / 2);
            ctx.textAlign = "right";
            ctx.fillStyle = "#fff";
            ctx.font = "bold 18px Arial";
            ctx.fillText(items[i], radius - 20, 5);
            ctx.restore();
            
            startAngle += sliceAngle;
        }}

        // 애니메이션이 끝나면 결과 표시 (Python 타임아웃과 얼추 맞춤)
        if ({str(is_spinning).lower()}) {{
            setTimeout(() => {{
                const resultText = document.getElementById('result');
                resultText.innerText = "🎉 당첨: " + items[{target_index}];
                resultText.style.animation = "pop 0.5s ease";
            }}, 4000);
        }}
    </script>
    """

# HTML 컴포넌트 렌더링
with col2:
    html_code = get_roulette_html(items, st.session_state.target_index, st.session_state.is_spinning)
    components.html(html_code, height=500)

# 결과 텍스트 표시 (파이썬 쪽)
if st.session_state.is_spinning:
    st.balloons() # 스크립트가 다시 실행될 때 풍선 효과

    # 다음 번 클릭을 위해 상태 초기화 버튼 (선택 사항)
    if st.button("다시 하기"):
        st.session_state.is_spinning = False
        st.rerun()
