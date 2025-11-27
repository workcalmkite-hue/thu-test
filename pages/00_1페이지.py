import streamlit as st
import pandas as pd

# --- 1. 메뉴 데이터 정의 ---
# 실제 롯데리아 메뉴를 참고하여 단순화된 딕셔너리 구조 사용
MENU_DATA = {
    "버거": [
        {"name": "불고기 버거", "price": 4500, "description": "달콤한 불고기 소스"},
        {"name": "새우 버거", "price": 4800, "description": "탱글탱글 새우 패티"},
        {"name": "클래식 치즈 버거", "price": 5000, "description": "순쇠고기와 고소한 치즈"}
    ],
    "세트": [
        {"name": "불고기 버거 세트", "price": 6800, "description": "버거+감자튀김+콜라"},
        {"name": "새우 버거 세트", "price": 7100, "description": "버거+감자튀김+콜라"},
        {"name": "핫 크리스피 버거 세트", "price": 7500, "description": "매콤한 치킨 패티 세트"}
    ],
    "디저트 & 사이드": [
        {"name": "양념감자", "price": 2000, "description": "시즈닝을 뿌려 먹는 감자"},
        {"name": "치즈 스틱", "price": 1800, "description": "쭉 늘어나는 치즈"},
        {"name": "롱 치즈 스틱", "price": 2500, "description": "더 길어진 치즈 스틱"}
    ],
    "음료": [
        {"name": "콜라", "price": 1800, "description": "시원한 탄산음료"},
        {"name": "사이다", "price": 1800, "description": "청량한 사이다"},
        {"name": "아메리카노", "price": 2500, "description": "따뜻하거나 차가운 커피"}
    ]
}

# --- 2. Streamlit Session State 초기화 (장바구니) ---
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'page' not in st.session_state:
    st.session_state.page = 'main' # 'main' 또는 'payment'

# --- 3. 핵심 함수 ---

def add_to_cart(menu_item):
    """선택된 메뉴를 장바구니에 추가하거나 수량을 증가시키는 함수"""
    found = False
    for item in st.session_state.cart:
        if item['name'] == menu_item['name']:
            item['qty'] += 1
            found = True
            break
    if not found:
        st.session_state.cart.append(
            {"name": menu_item['name'], "price": menu_item['price'], "qty": 1}
        )
    st.toast(f"✅ 장바구니에 '{menu_item['name']}' 1개를 추가했습니다!", icon='🛒')

def calculate_total():
    """장바구니의 총액을 계산하는 함수"""
    total = sum(item['price'] * item['qty'] for item in st.session_state.cart)
    return total

def change_qty(item_name, delta):
    """장바구니 항목의 수량을 변경하는 함수"""
    for i, item in enumerate(st.session_state.cart):
        if item['name'] == item_name:
            item['qty'] += delta
            if item['qty'] <= 0:
                del st.session_state.cart[i] # 수량이 0 이하면 장바구니에서 제거
                st.toast(f"🗑️ '{item_name}'을(를) 장바구니에서 제거했습니다.", icon='🚨')
            break

def go_to_payment():
    """결제 페이지로 이동"""
    if st.session_state.cart:
        st.session_state.page = 'payment'
    else:
        st.warning("장바구니가 비어있습니다. 메뉴를 선택해주세요.")

def back_to_main():
    """메인 메뉴 선택 페이지로 복귀"""
    st.session_state.page = 'main'
    
def complete_order():
    """주문 완료 및 장바구니 초기화"""
    st.balloons()
    st.session_state.cart = []
    st.session_state.page = 'main'
    st.success("🎉 주문이 완료되었습니다! 잠시 후 메인 화면으로 돌아갑니다.")
    # 3초 후 메인으로 돌아가게 설정 (실제 Streamlit 환경에서는 바로 동작)
    # st.experimental_rerun()

# --- 4. UI 렌더링 함수 ---

def render_menu_selection():
    """메인 메뉴 선택 화면 (왼쪽)"""
    st.header("1. 메뉴 선택하기", divider='orange')

    # 카테고리 탭 생성
    categories = list(MENU_DATA.keys())
    tabs = st.tabs(categories)

    for tab, category in zip(tabs, categories):
        with tab:
            st.subheader(f"🍔 {category}")
            col1, col2 = st.columns(2)
            
            # 메뉴 항목을 두 열로 나누어 표시
            menu_items = MENU_DATA[category]
            
            for i, item in enumerate(menu_items):
                col = col1 if i % 2 == 0 else col2
                with col:
                    # 메뉴 카드 스타일링
                    with st.container(border=True):
                        st.markdown(f"**{item['name']}**")
                        st.markdown(f"**{item['price']:,}원**")
                        st.caption(item['description'])
                        st.button(
                            f"담기", 
                            key=f"{category}_{item['name']}", 
                            on_click=add_to_cart, 
                            args=(item,),
                            use_container_width=True
                        )

def render_cart_and_summary():
    """장바구니 및 총액 표시 화면 (오른쪽)"""
    st.header("2. 주문 내용 확인", divider='orange')

    total_amount = calculate_total()
    
    # 장바구니 내용
    if not st.session_state.cart:
        st.info("장바구니가 비어 있습니다. 메뉴를 선택해주세요.")
    else:
        cart_df = pd.DataFrame(st.session_state.cart)
        cart_df['소계'] = cart_df['price'] * cart_df['qty']
        
        # Streamlit의 data_editor를 사용하여 수량 변경 가능하도록 설정
        edited_df = st.data_editor(
            cart_df[['name', 'qty', 'price', '소계']],
            column_config={
                "name": st.column_config.TextColumn("메뉴", disabled=True),
                "qty": st.column_config.NumberColumn("수량", min_value=1, step=1, default=1),
                "price": st.column_config.NumberColumn("단가 (원)", format="%,d", disabled=True),
                "소계": st.column_config.NumberColumn("소계 (원)", format="%,d", disabled=True),
            },
            hide_index=True,
            use_container_width=True,
            key='cart_editor'
        )
        
        # data_editor의 변경 사항을 Session State에 반영
        # Streamlit data_editor는 편집 시 새 DataFrame을 반환하므로 이를 처리해야 함
        if edited_df is not None:
             # 편집된 데이터프레임을 기반으로 장바구니 갱신
            new_cart = []
            for index, row in edited_df.iterrows():
                if row['qty'] > 0:
                    new_cart.append({
                        "name": row['name'], 
                        "price": row['price'], 
                        "qty": row['qty']
                    })
            st.session_state.cart = new_cart
        
    st.divider()

    # 최종 금액 표시 및 결제 버튼
    st.metric(
        label="💰 총 주문 금액", 
        value=f"{total_amount:,}원", 
        delta_color="off"
    )
    
    st.button(
        "➡️ 주문 완료 및 결제", 
        on_click=go_to_payment, 
        use_container_width=True, 
        type="primary"
    )
    st.caption("결제 페이지로 이동합니다.")


def render_payment_page():
    """결제 화면"""
    st.title("💳 결제하기")
    
    total_amount = calculate_total()
    
    st.subheader(f"최종 결제 금액: **{total_amount:,}원**")
    
    st.markdown("---")
    st.info("⚠️ **주의:** 이 페이지는 키오스크 시뮬레이션이며, **실제 결제가 이루어지지 않습니다.**")

    # 결제 수단 선택 (UI 단순화)
    payment_method = st.radio(
        "결제 수단을 선택해 주세요:",
        ["신용카드 / 체크카드", "간편 결제 (Pay)", "상품권 / 쿠폰"],
        index=0
    )
    
    st.warning(f"선택하신 수단: **{payment_method}**")

    # 결제 완료 버튼
    st.button(
        f"✅ {payment_method}으로 결제 완료", 
        on_click=complete_order, 
        use_container_width=True, 
        type="primary"
    )
    
    st.button("⬅️ 메뉴 수정하기", on_click=back_to_main, use_container_width=True)


# --- 5. 메인 앱 실행 로직 ---

st.set_page_config(
    page_title="Streamlit 키오스크 시뮬레이터",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    /* Streamlit 앱의 배경색을 키오스크처럼 밝게 변경 (선택사항) */
    .stApp {
        background-color: #f7f7f7;
    }
    /* 타이틀에 로고 느낌 추가 */
    h1 {
        text-align: center;
        color: #e51f28; /* 롯데리아 상징색 */
        border: 2px solid #e51f28;
        padding: 10px;
        border-radius: 10px;
        background-color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🍔 롯데리아 스타일 키오스크 시뮬레이터")

if st.session_state.page == 'main':
    # 메인 페이지: 메뉴 선택 및 장바구니
    col_menu, col_cart = st.columns([2, 1])
    
    with col_menu:
        render_menu_selection()

    with col_cart:
        render_cart_and_summary()

elif st.session_state.page == 'payment':
    # 결제 페이지
    render_payment_page()
