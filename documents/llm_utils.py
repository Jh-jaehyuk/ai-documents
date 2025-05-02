from ollama import ChatResponse, chat


def summarize_with_ollama(content: str, model: str = "gemma3:4b-it-qat") -> str:
    prompt = (f"다음 문서를 한국어로 간결하게 요약해줘:\n\n{content}\n\n"
              f"단, 요약이 의미 없는 문장일 경우 너의 판단에 따라 '의미 없는 문서입니다.' 또는 '테스트용 문서입니다.' 라고 작성해.")

    response: ChatResponse = chat(
        model=model,
        messages=[
            {
                'role': 'user',
                'content': prompt
            },
        ],
        stream=False
    )

    return response.message.content

def extract_keywords(summary: str) -> list:
    import re

    # LLM을 이용해서 키워드를 뽑아내야하지만, 테스트용이므로 문장 내에서 최대 5개의 단어를 추출하도록 함
    words = re.findall(r'\b[가-힣a-zA-Z]{2,}\b', summary)

    return list(set(words))[:5]
