import streamlit as st
from openai import OpenAI

# Show title and description.
st.title("💬 Chatbot")
st.write(
    "안녕하세요 C: 귀여운 문도리의 호주 시드니 여행 가이드 서비스는 OpenAI의 GPT-3.5 모델을 활용하여, 여러분의 여행을 더욱 즐겁고 편리하게 만들어주는 스마트 챗봇입니다."
    "간단히 OpenAI API 키만 입력하면 바로 이용하실 수 있어요."
)

# 🐨 시드니 소개 추가
st.markdown("""
### 🇦🇺 시드니는 어떤 곳인가요?

시드니는 호주의 대표적인 도시이자, 세계적으로 사랑받는 여행지예요.  
아름다운 해변, 웅장한 오페라 하우스, 다양한 문화와 맛집, 그리고 여유로운 라이프스타일까지 모두 갖춘 도시랍니다.

🌊 **본다이 비치**에서 서핑을 즐기고,  
🎭 **오페라 하우스** 앞에서 인증샷도 남기고,  
🌉 **하버 브리지**를 건너며 멋진 일몰을 감상해보세요.

시드니는 혼자 여행하든, 연인이든, 가족이든 모두를 만족시켜줄 매력적인 도시예요.  
지금 바로 나만의 시드니 여행을 계획해보세요!
""")

# 🗝️ 사용자로부터 OpenAI API 키 입력 받기
openai_api_key = st.text_input("OpenAI API Key를 입력하세요", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:

    # Create an OpenAI client.
    client = OpenAI(api_key=openai_api_key)

     # 여행 기간 선택
    travel_days = st.slider("⏳ 여행은 얼마나 떠나실 예정인가요?", min_value=1, max_value=14, value=4)
    
    # 여행 스타일 선택
    with st.expander("🎒 여행 스타일을 선택해 주세요"):
        travel_styles = st.multiselect(
            "원하는 여행 스타일을 선택하세요 (복수 선택 가능)",
            ["맛집 탐방", "자연 힐링", "문화 체험", "사진 찍기", "쇼핑", "혼자 여행", "가족 여행", "커플 여행"]
        )

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # 사용자 입력이 아닌 버튼 클릭으로 질문 보내기
    if st.button("🗺️ 나만의 여행 일정 추천받기"):
        user_prompt = f"""
        저는 {travel_days}일 동안 시드니 여행을 할 예정입니다.
        여행 스타일은 {', '.join(travel_styles)} 입니다.
        이 스타일에 맞는 여행 일정과 추천 장소를 알려주세요.
        """

    st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        # GPT 호출
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # 응답 출력 및 저장
        with st.chat_message("assistant"):
            response = st.write_stream(stream)

        st.session_state.messages.append({"role": "assistant", "content": response})
    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("호주 시드니 여행이 궁금한가요? 질문을 입력해 보세요!"):

        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate a response using the OpenAI API.
        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )

        # Stream the response to the chat using `st.write_stream`, then store it in 
        # session state.
        with st.chat_message("assistant"):
            response = st.write_stream(stream)
        st.session_state.messages.append({"role": "assistant", "content": response})
