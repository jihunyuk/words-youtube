import streamlit as st
import pandas as pd
import data
from urllib.parse import quote_plus

st.set_page_config(page_title="토익 기출 단어장", page_icon="🔥", layout="centered")

st.markdown(
    """
    <style>
    .block-container { padding-top: 20px; }

    div[data-testid='stTable'] table { font-size: 0.9rem; }

    .word-table table { font-size: 0.9rem; }
    .word-table th { text-align: left; }
    .word-table td:nth-child(3) { font-size: 0.7rem; }

    .flashcard-wrap { margin-top: 2px; }
    div[data-testid='stExpander'] div { padding-top: 0 !important; }

    .flashcard-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        margin: 0;
        padding: 0;
    }

    .meaning-text {
        font-size: 0.75rem;
        line-height: 1.35;
        flex: 1;
    }

    .pronounce-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        min-width: 32px;
        height: 32px;
        padding: 0 8px;
        background: rgba(128,128,128,0.16);
        border: 1px solid rgba(128,128,128,0.22);
        border-radius: 10px;
        text-decoration: none;
        font-size: 14px;
        line-height: 1;
        color: inherit;
        white-space: nowrap;
        flex-shrink: 0;
        transition: background 0.15s ease;
    }

    .pronounce-pill:hover {
        background: rgba(128,128,128,0.28);
    }

    </style>
    """,
    unsafe_allow_html=True
)

@st.cache_data
def load_vocab():
    vocab_dict = {}
    for i in range(1, 31):
        var_name = f"dat_{i}"
        if hasattr(data, var_name):
            vocab_dict[f"Day {i:02d}"] = getattr(data, var_name)
    return vocab_dict

vocab_dict = load_vocab()


def sidebar_compact_divider():
    st.sidebar.markdown(
        "<hr style='margin:0.25rem 0 0.5rem 0;border:none;border-top:1px solid rgba(128,128,128,0.35);'>",
        unsafe_allow_html=True,
    )


def is_idiom(text: str) -> bool:
    return " " in text.strip()


def format_meaning_html(text: str):
    return "<br>".join([t.strip() for t in text.split("/")])


def render_flashcard(word: str, meaning: str):
    formatted_meaning = format_meaning_html(meaning)

    if is_idiom(word):
        with st.expander(f"**{word}**"):
            html = f"""
            <div class='flashcard-wrap'>
                <div class='flashcard-row'>
                    <div class='meaning-text'>{formatted_meaning}</div>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)
    else:
        search_url = f"https://www.google.com/search?q={quote_plus(word + ' 발음')}"
        with st.expander(f"**{word}**"):
            html = f"""
            <div class='flashcard-wrap'>
                <div class='flashcard-row'>
                    <div class='meaning-text'>{formatted_meaning}</div>
                    <a class='pronounce-pill' href='{search_url}' target='_blank'>🔊</a>
                </div>
            </div>
            """
            st.markdown(html, unsafe_allow_html=True)


st.sidebar.title("🔥 토익 단어 마스터")
st.sidebar.markdown("서아쌤의 비밀과외 기출 보카")
sidebar_compact_divider()

mode = st.sidebar.radio("학습 모드", ["단어장 보기 (Table)", "암기 테스트 (Flashcard)"])

if "day_state" not in st.session_state:
    st.session_state.day_state = 1

st.sidebar.markdown("### 학습할 Day")
st.sidebar.slider("Day 선택", 1, 30, key="day_state")

day = st.session_state.day_state
selected_day = f"Day {day:02d}"

sidebar_compact_divider()
st.sidebar.caption("파이썬과 Streamlit으로 제작되었습니다. 🚀")

st.header(selected_day)

current_data = vocab_dict[selected_day]

if mode == "단어장 보기 (Table)":
    df = pd.DataFrame(current_data, columns=["단어 및 숙어", "뜻"])
    df["뜻"] = df["뜻"].str.replace("/", "<br>", regex=False)
    df.index = df.index + 1
    st.markdown(f"<div class='word-table'>{df.to_html(escape=False)}</div>", unsafe_allow_html=True)

elif mode == "암기 테스트 (Flashcard)":
    for word, meaning in current_data:
        render_flashcard(word, meaning)

st.markdown("---")


def prev_day():
    if st.session_state.day_state > 1:
        st.session_state.day_state -= 1


def next_day():
    if st.session_state.day_state < 30:
        st.session_state.day_state += 1

# simplest navigation (may stack vertically on mobile)
st.button("◀ 이전", on_click=prev_day, disabled=(day == 1), key="prev")
st.button("다음 ▶", on_click=next_day, disabled=(day == 30), key="next")