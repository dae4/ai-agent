# agent.py (Local LLM 버전)
import os
import json
from openai import OpenAI  # 라이브러리는 그대로 사용 (OpenAI 호환 API 사용)
from tools import AVAILABLE_TOOLS

class SimpleAgent:
    def __init__(self):
        # [핵심 변경 포인트 1] base_url을 내 로컬 주소로 변경
        # [핵심 변경 포인트 2] api_key는 아무거나 넣어도 됨 (로컬이라 인증 불필요)
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama" 
        )
        
        # [핵심 변경 포인트 3] 로컬 모델 이름 지정
        self.model_name = "llama3.1" 

        # 로컬 모델은 GPT-4보다 멍청할 수 있으므로, 프롬프트를 더 강력하게 줍니다.
        self.system_prompt = """
        You are a smart AI assistant. You MUST reply in valid JSON format.
        
        Available Tools:
        - get_current_time: Use this to get current time. (No arguments)
        - calculate_length: Use this to count characters in text. (Arguments: text)

        Response Format (Strict JSON):
        If you need to use a tool:
        { "type": "action", "function": "function_name", "input": "input_value" }
        
        If you have the answer:
        { "type": "final_answer", "content": "your final answer here" }
        """

    def think_and_act(self, user_query):
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_query}
        ]

        print(f"🤖 사용자 질문 (Local): {user_query}")

        for i in range(5):
            try:
                # API 호출
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                    response_format={"type": "json_object"}, # Llama3도 JSON 모드 지원함
                    temperature=0 # 창의성 0으로 설정 (정확한 JSON 출력을 위해)
                )
                
                result_text = response.choices[0].message.content
                
                # 가끔 로컬 모델이 JSON 외의 잡담을 섞을 때가 있어 파싱 에러 방지
                try:
                    result_json = json.loads(result_text)
                except json.JSONDecodeError:
                    # 실패 시 간단한 복구 시도 (혹은 로그 출력)
                    print(f"  ⚠ JSON 파싱 실패, 재시도 중...: {result_text}")
                    continue

                # 2. 최종 답변인지 확인
                if result_json.get("type") == "final_answer":
                    return result_json["content"]

                # 3. 도구 사용 요청이면
                elif result_json.get("type") == "action":
                    func_name = result_json["function"]
                    func_input = result_json["input"]
                    
                    print(f"  [Step {i+1}] 로컬AI 생각: {func_name} 도구 사용")
                    
                    tool_function = AVAILABLE_TOOLS.get(func_name)
                    if tool_function:
                        observation = tool_function(func_input)
                        print(f"  → 결과: {observation}")
                        
                        messages.append({"role": "assistant", "content": result_text})
                        messages.append({"role": "user", "content": f"Tool Output: {observation}"})
                    else:
                        print("  → 에러: 없는 도구입니다.")
                        break
            except Exception as e:
                print(f"에러 발생: {e}")
                break
        
        return "해결 실패"