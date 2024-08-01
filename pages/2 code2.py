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

def try_generate_content(api_key, prompt):
    genai.configure(api_key=api_key)
   
    model = genai.GenerativeModel(model_name="gemini-1.0-pro",
                                  generation_config={
                                      "temperature": 0.9,
                                      "top_p": 1,
                                      "top_k": 1,
                                      "max_output_tokens": 2048,
                                  },
                                  safety_settings=[
                                      {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                      {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                                  ])
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"API 호출 실패: {e}")
        return None

st.title("산소의 역할 피드백 웹앱")
st.write("산소가 우리 삶에 미치는 역할에 대한 답변을 입력하고 피드백을 받아보세요.")

user_input = st.text_area("답변을 입력하세요:", placeholder="예: 산소는 생명 유지에 필수적입니다...")

if st.button("피드백 받기"):
    if user_input:
        feedback = try_generate_content(api_key, user_input)
        if feedback:
            st.markdown(to_markdown(feedback))
        else:
            st.error("피드백을 생성하는 데 실패했습니다. 다시 시도해주세요.")
    else:
        st.warning("답변을 입력해주세요.")
