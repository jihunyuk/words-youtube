import streamlit as st
import pandas as pd
import data  # 같은 폴더에 있는 data.py 파일을 불러옵니다.

# 1. 페이지 설정
st.set_page_config(
    page_title="토익 기출 단어장",
    page_icon="🔥",
    layout="centered"
)

# 2. data.py에서 dat_1 ~ dat_30까지의 데이터를 동적으로 불러와 딕셔너리로 묶기
vocab_dict = {}
for i in range(1, 31):
    var_name = f"dat_{i}"
    # data.py 내에 dat_n 변수가 있는지 확인하고 가져옵니다.
    if hasattr(data, var_name):
        vocab_dict[f"Day {i:02d}"] = getattr(data, var_name)

# 3. 사이드바 구성 (메뉴)
st.sidebar.title("🔥 토익 단어 마스터")
st.sidebar.markdown("서아쌤의 비밀과외 기출 보카")
st.sidebar.divider()

# 학습할 일차 선택
selected_day = st.sidebar.selectbox("학습할 일차를 선택하세요", list(vocab_dict.keys()))

# 학습 모드 선택
mode = st.sidebar.radio("학습 모드", ["단어장 보기 (Table)", "암기 테스트 (Flashcard)"])

st.sidebar.divider()
st.sidebar.caption("파이썬과 Streamlit으로 제작되었습니다. 🚀")

# 4. 메인 화면 구성
st.title(f"📖 {selected_day} 학습하기")
st.markdown("매일매일 꾸준히 반복해서 학습해 보세요!")

# 선택된 일차의 데이터 가져오기
current_data = vocab_dict[selected_day]

# 5. 모드별 화면 렌더링
if mode == "단어장 보기 (Table)":
    # Pandas DataFrame으로 변환하여 깔끔한 표 형태로 보여줍니다.
    df = pd.DataFrame(current_data, columns=["단어 / 숙어", "뜻"])
    df.index = df.index + 1  # 인덱스를 1부터 시작하도록 조정
    
    st.table(df)

elif mode == "암기 테스트 (Flashcard)":
    st.info("💡 단어를 보고 뜻을 먼저 떠올려 본 뒤, 탭을 눌러 정답을 확인하세요.")
    
    # Streamlit의 expander 기능을 이용해 플래시카드 형태 구현
    for word, meaning in current_data:
        with st.expander(f"**{word}**"):
            st.success(f"👉 {meaning}")