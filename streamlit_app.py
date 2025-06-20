import streamlit as st
from openai import OpenAI
import time

# 페이지 설정
st.set_page_config(
    page_title="달리기 훈련 챗봇",
    page_icon="🏃‍♂️",
    layout="wide"
)

# 앱 제목과 설명
st.title("🏃‍♂️ 달리기 훈련 챗봇")
st.write(
    "OpenAI GPT-4o 모델을 이용한 전문 달리기 트레이너 챗봇입니다. "
    "달리기 실력 향상을 위한 조언, 운동 프로그램, 부상 예방 등에 대해 물어보세요!"
)

# 사이드바에 정보 추가
with st.sidebar:
    st.header("📖 사용 가이드")
    st.write("""
    **질문 예시:**
    - 초보자를 위한 달리기 프로그램
    - 5km 달리기 시간 단축 방법
    - 달리기 부상 예방법
    - 달리기 후 스트레칭 방법
    - 마라톤 준비 계획
    """)
    
    st.header("⚠️ 주의사항")
    st.write("""
    - 의학적 조언이 필요한 경우 전문의와 상담하세요
    - 개인의 체력 수준을 고려하여 운동하세요
    - 부상이 있을 때는 무리하지 마세요
    """)

# OpenAI API 키 입력받기
openai_api_key = st.text_input("🔐 OpenAI API Key 입력", type="password", help="OpenAI 웹사이트에서 발급받은 API 키를 입력하세요")

# API 키가 없을 경우 안내
if not openai_api_key:
    st.info("계속하려면 OpenAI API 키를 입력해주세요.", icon="🔑")
    st.markdown("""
    **API 키 발급 방법:**
    1. [OpenAI 웹사이트](https://platform.openai.com/)에 가입
    2. API Keys 메뉴에서 새 키 생성
    3. 생성된 키를 위의 입력창에 붙여넣기
    """)
    st.stop()

# OpenAI 클라이언트 생성
try:
    client = OpenAI(api_key=openai_api_key)
except Exception as e:
    st.error(f"OpenAI 클라이언트 생성 중 오류가 발생했습니다: {str(e)}")
    st.stop()

# 세션 상태 초기화 (이전 대화 저장용)
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": """너는 전문 러닝 코치이자 트레이너야. GPT-4o의 고급 능력을 활용해서 다음 지침을 따라 답변해줘:

1. 달리기 실력 향상을 위한 구체적이고 실용적인 조언 제공
2. 사용자의 현재 수준을 고려한 맞춤형 프로그램 제안
3. 안전과 부상 예방을 항상 강조
4. 과학적 근거와 최신 스포츠 과학 지식 활용
5. 필요시 점진적인 훈련 계획을 주차별로 상세히 제시
6. 영양, 휴식, 정신적 측면도 고려한 종합적 조언
7. 개인차를 고려한 다양한 대안 제시
8. 복잡한 질문에 대해서는 단계별로 자세히 설명

한국어로 답변하고, 이모지를 적절히 사용해서 친근하면서도 전문적으로 대화해줘."""
        }
    ]

# 대화 초기화 버튼
if st.button("🔄 새 대화 시작", help="대화 기록을 초기화합니다"):
    st.session_state.messages = st.session_state.messages[:1]  # 시스템 메시지만 유지
    st.rerun()

# 이전 대화 출력
for msg in st.session_state.messages[1:]:  # system 메시지는 제외하고 표시
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 사용자 입력 받기
if user_input := st.chat_input("무엇이 궁금한가요? 예: 달리기 속도 올리는 법 알려줘"):
    
    # 사용자 메시지 저장 및 출력
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # OpenAI 응답 생성 (스트리밍)
    try:
        with st.chat_message("assistant"):
            with st.spinner("답변을 생성하고 있습니다..."):
                stream = client.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages,
                    stream=True,
                    temperature=0.7,  # 창의적이면서도 일관된 답변
                    max_tokens=1500,  # GPT-4o에 맞춰 토큰 수 증가
                )
                
                response = st.write_stream(stream)
        
        # 응답을 세션 상태에 저장
        st.session_state.messages.append({"role": "assistant", "content": response})
        
    except Exception as e:
        st.error(f"응답 생성 중 오류가 발생했습니다: {str(e)}")
        st.info("API 키가 올바른지 확인하고, 잠시 후 다시 시도해주세요.")

# 푸터
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray;'>
        💡 건강한 달리기 생활을 위해 항상 안전을 우선시하세요!<br>
        Made with ❤️ using Streamlit & OpenAI GPT-4o
    </div>
    """, 
    unsafe_allow_html=True
)
