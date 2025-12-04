# main.py
from dotenv import load_dotenv
from agent import SimpleAgent

# .env 파일 로드
load_dotenv()

def main():
    bot = SimpleAgent()
    
    # 테스트 1: 시간 확인
    print("\n--- Test 1 ---")
    result1 = bot.think_and_act("지금 몇 시야?")
    print(f"🏁 최종 답변: {result1}")

    # 테스트 2: 복합 추론
    print("\n--- Test 2 ---")
    # LLM은 'hello world'의 길이를 모르지만, 도구를 써서 알아올 것임
    result2 = bot.think_and_act("'hello world'라는 글자가 몇 글자인지 세어줘")
    print(f"🏁 최종 답변: {result2}")

if __name__ == "__main__":
    main()