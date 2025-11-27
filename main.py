import streamlit as st

def get_divisors(number):
    """
    입력된 숫자의 약수를 찾아 리스트로 반환하는 함수
    """
    if number <= 0:
        return []
        
    divisors = []
    # 1부터 number의 제곱근까지 반복
    for i in range(1, int(number**0.5) + 1):
        if number % i == 0:
            divisors.append(i)
            # i가 number의 제곱근이 아니라면, 몫(number // i)도 약수임
            if i * i != number:
                divisors.append(number // i)
                
    # 약수를 오름차순으로 정렬
    divisors.sort()
    return divisors

## --- Streamlit UI 구성 ---

st.title("🔢 약수 찾기 웹 앱")
st.markdown("숫자를 입력하면 해당 숫자의 모든 약수를 찾아 드립니다.")

# 사용자로부터 숫자 입력 받기
number_input = st.number_input(
    "양의 정수를 입력하세요:", 
    min_value=1, 
    value=100, 
    step=1,
    format="%d"
)

# 입력된 숫자가 유효한 정수인지 확인
if number_input is not None and number_input >= 1:
    try:
        # number_input은 float으로 반환될 수 있으므로 정수로 변환
        number = int(number_input)
        
        # 약수 계산
        divisors_list = get_divisors(number)
        
        st.subheader(f"✨ 입력된 숫자: **{number}**")
        
        if divisors_list:
            st.success(f"**{number}**의 약수 개수: **{len(divisors_list)}**개")
            
            # 결과를 보기 좋게 출력
            st.markdown("### 📝 약수 목록")
            # 쉼표로 구분하여 문자열로 만들고 출력
            divisors_str = ", ".join(map(str, divisors_list))
            st.code(divisors_str)
            
            # 참고: 리스트 형태로도 보여줄 수 있습니다.
            # st.write(divisors_list)
            
        else:
            # 이 경우는 number_input의 min_value 때문에 사실상 도달하기 어려움
            st.warning("유효한 양의 정수를 입력해 주세요.")
            
    except ValueError:
        st.error("숫자 입력이 잘못되었습니다. 정수를 입력해 주세요.")

st.markdown(
    """
    ---
    *Streamlit Cloud 배포용*
    """
)
