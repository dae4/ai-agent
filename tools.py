# tools.py
import datetime

def get_current_time(args=None):
    """현재 시간을 알려주는 도구"""
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def calculate_length(text):
    """글자 수를 세어주는 도구"""
    return len(str(text))

# 도구들을 딕셔너리로 관리 (에이전트가 이름을 보고 찾을 수 있게)
AVAILABLE_TOOLS = {
    "get_current_time": get_current_time,
    "calculate_length": calculate_length
}