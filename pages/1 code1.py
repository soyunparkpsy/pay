import textwrap
import google.generativeai as genai
import streamlit as st
import toml
import pathlib

def to_markdown(text):
    text = text.replace('•', '*')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# secrets.toml 파일 경로
secrets_path = pathlib.Path(__file__).parent.parent / ".streamlit/secrets.toml"

# secrets.toml 파일 읽기
with open(secrets_path, "r") as f:
    secrets = toml.load(f)

# secrets.toml 파일에서 API 키 값 가져오기
api_key = secrets.get("api_key")

# few-shot 프롬프트 구성 함수 수정
def try_generate_content(api_key, prompt):
    # API 키를 설정
    genai.configure(api_key=api_key)
   
    # 설정된 모델 변경
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config={
                                      "temperature": 0.7,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 512,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        # 콘텐츠 생성 시도
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        # 예외 발생시 None 반환
        print(f"API 호출 실패: {e}")
        return None

# Streamlit 앱 시작
st.title("원소 정보 제공기")
st.write("원소 이름을 입력하면 해당 원소의 특징과 우리 생활에서 주로 사용되는 물질을 알려드립니다. 🌟")

# 원소 이름 입력 받기
element_name = st.text_input("원소 이름을 입력하세요", "")

if element_name:
    prompt = f"{element_name} 원소의 특징과 우리 생활에서 많이 사용하는 물질을 설명해주세요."
    content = try_generate_content(api_key, prompt)

    if content:
        st.markdown(to_markdown(content))
    else:
        st.error("정보를 불러오는데 실패했습니다. 나중에 다시 시도해주세요.")
