import streamlit as st
import os
from openai import OpenAI

# 💬 앱 제목과 소개
st.title("💬 시드니 여행 가이드 챗봇")
st.write(
    "안녕하세요 C: 귀여운 문도리의 호주 시드니 여행 가이드는 GPT-3.5를 기반으로 여러분의 여행을 더 똑똑하고 즐겁게 만들어줄 스마트 챗봇이에요!"
)

# 🇦🇺 시드니 소개
st.markdown("""
### 🐨 시드니는 어떤 곳인가요?

시드니는 호주의 대표적인 도시이자, 세계적으로 사랑받는 여행지예요.  
아름다운 해변, 웅장한 오페라 하우스, 다양한 문화와 맛집, 그리고 여유로운 라이프스타일까지 모두 갖춘 도시랍니다.

🌊 **본다이 비치**에서 서핑을 즐기고,  
🎭 **오페라 하우스** 앞에서 인증샷도 남기고,  
🌉 **하버 브리지**를 건너며 멋진 일몰을 감상해보세요.

혼자, 친구와, 가족과도 모두 찰떡인 도시예요 🧡  
""")

# 🔐 OpenAI API 키 입력
openai_api_key = st.text_input("🔑 OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("OpenAI API 키를 입력해야 챗봇을 사용할 수 있어요!", icon="🔑")
    st.stop()
else:
    os.environ["OPENAI_API_KEY"] = openai_api_key  # 환경변수 설정
    client = OpenAI()  # 환경변수에서 키 자동 인식

# 🧳 여행 옵션 받기
travel_days = st.slider("⏳ 여행은 며칠 예정인가요?", 1, 14, 4)

with st.expander("🎒 어떤 스타일의 여행을 원하시나요?"):
    travel_styles = st.multiselect(
        "복수 선택 가능!",
        ["맛집 탐방", "자연 힐링", "문화 체험", "사진 찍기", "쇼핑", "혼자 여행", "가족 여행", "커플 여행"]
    )

# 💬 메시지 상태 저장
if "messages" not in st.session_state:
    st.session_state.messages = []

# 이전 대화 보여주기
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 📩 여행 일정 추천 버튼
if st.button("🗺️ 나만의 여행 일정 추천받기"):
    if not travel_styles:
        st.warning("여행 스타일을 한 가지 이상 선택해 주세요!")
    else:
        user_prompt = f"""
        저는 {travel_days}일 동안 시드니 여행을 할 예정입니다.
        여행 스타일은 {', '.join(travel_styles)} 입니다.
        이 스타일에 맞는 여행 일정과 추천 장소를 알려주세요.
        """
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        try:
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            with st.chat_message("assistant"):
                response = st.write_stream(stream)

            st.session_state.messages.append({"role": "assistant", "content": response})

        except Exception as e:
            st.error(f"에러가 발생했어요: {e}")

# 💬 자유 입력 질문도 가능!
if prompt := st.chat_input("호주 시드니 여행이 궁금한가요? 자유롭게 질문해보세요!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})

    except Exception as e:
        st.error(f"에러가 발생했어요: {e}")
