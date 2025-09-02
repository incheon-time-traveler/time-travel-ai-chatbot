from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages

# 상태 정의
class State(TypedDict):
    # 메시지 정의하기
    messages: Annotated[list, add_messages]
    question_analysis: dict  # 질문 분석 결과
    current_step: str  # 현재 처리 단계