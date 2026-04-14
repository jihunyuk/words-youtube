import streamlit as st
import pandas as pd
import data
from urllib.parse import quote_plus

st.set_page_config(page_title="토익 기출 단어장", page_icon="🔥", layout="centered")

st.markdown("""
<style>
.block-container { padding-top: 20px; }
.word-table table { font-size:0.9rem; }
.word-table th { text-align:left; }
.word-table td:nth-child(2){ font-size:0.7rem; }
.flashcard-row{display:flex;justify-content:space-between;align-items:center;gap:8px;margin:0;padding:0}
.meaning-text{font-size:0.75rem;line-height:1.35;flex:1}
.pronounce-pill{display:inline-flex;align-items:center;justify-content:center;min-width:32px;height:32px;padding:0 8px;background:rgba(128,128,128,0.16);border:1px solid rgba(128,128,128,0.22);border-radius:10px;text-decoration:none;font-size:14px;color:inherit;white-space:nowrap}
</style>
""",unsafe_allow_html=True)

@st.cache_data
def load_vocab():
    vocab_dict={}
    for i in range(1,31):
        var_name=f"dat_{i}"
        if hasattr(data,var_name):
            vocab_dict[f"Day {i:02d}"]=getattr(data,var_name)
    return vocab_dict

vocab_dict=load_vocab()


def format_meaning_html(text:str):
    return "<br>".join([t.strip() for t in text.split("/")])


def render_flashcard(word:str,meaning:str):
    formatted=format_meaning_html(meaning)
    search_url=f"https://www.google.com/search?q={quote_plus(word+' 발음')}"
    with st.expander(f"**{word}**"):
        html=f"""
        <div class='flashcard-row'>
            <div class='meaning-text'>{formatted}</div>
            <a class='pronounce-pill' href='{search_url}' target='_blank'>🔊</a>
        </div>
        """
        st.markdown(html,unsafe_allow_html=True)

st.sidebar.title("🔥 토익 단어 마스터")
st.sidebar.markdown("서아쌤의 비밀과외 기출 보카")

mode=st.sidebar.radio("학습 모드",["단어장 보기 (Table)","암기 테스트 (Flashcard)"])

if "day_state" not in st.session_state:
    st.session_state.day_state=1

st.sidebar.slider("Day 선택",1,30,key="day_state")

day=st.session_state.day_state
selected_day=f"Day {day:02d}"

st.header(selected_day)

current_data=vocab_dict[selected_day]

if mode=="단어장 보기 (Table)":
    df=pd.DataFrame(current_data,columns=["단어 및 숙어","뜻"])
    df["뜻"]=df["뜻"].str.replace("/","<br>",regex=False)
    df.index=df.index+1
    st.markdown(f"<div class='word-table'>{df.to_html(escape=False)}</div>",unsafe_allow_html=True)

elif mode=="암기 테스트 (Flashcard)":
    for word,meaning in current_data:
        render_flashcard(word,meaning)

st.markdown("---")


def prev_day():
    if st.session_state.day_state>1:
        st.session_state.day_state-=1


def next_day():
    if st.session_state.day_state<30:
        st.session_state.day_state+=1

st.button("◀ 이전",on_click=prev_day,disabled=(day==1))
st.button("다음 ▶",on_click=next_day,disabled=(day==30))
