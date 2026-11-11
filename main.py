import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices  # 리스트 형태 (4개)
        self.answer = answer    # 정수 형태 (1~4)

    def display(self, index):
        """문제를 화면에 출력합니다."""
        print(f"\n문제 {index}: {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        """정답 여부를 확인합니다."""
        return user_answer == self.answer

def get_safe_input(prompt, min_val, max_val):
    """
    공백 제거, 숫자 변환, 범위 검증, 빈 입력 처리를 포함한 안전한 입력 함수
    """
    while True:
        try:
            user_input = input(prompt).strip() # 앞뒤 공백 제거
            
            if not user_input:
                print(">> [오류] 입력값이 비어 있습니다. 다시 입력해 주세요.")
                continue
            
            val = int(user_input) # 숫자 변환 시도
            
            if min_val <= val <= max_val:
                return val
            else:
                print(f">> [오류] {min_val}에서 {max_val} 사이의 숫자를 입력해 주세요.")
        
        except ValueError:
            print(">> [오류] 숫자가 아닌 값이 입력되었습니다. 다시 입력해 주세요.")

def load_data():
    """파일이 없거나 손상된 경우 기본 데이터를 반환합니다."""
    default_quizzes = [
        Quiz("파이썬의 창시자는?", ["귀도 반 로섬", "제임스 고슬링", "데니스 리치", "빌 게이츠"], 1),
        Quiz("Git에서 저장소를 초기화하는 명령어는?", ["git push", "git commit", "git init", "git pull"], 3)
    ]
    
    file_path = "quizzes.json"
    
    if not os.path.exists(file_path):
        print("\n[알림] 데이터 파일이 없어 기본 퀴즈를 로드합니다.")
        return default_quizzes

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # JSON 데이터를 Quiz 객체 리스트로 변환
            return [Quiz(q['question'], q['choices'], q['answer']) for q in data]
    except (json.JSONDecodeError, KeyError):
        print("\n[경고] 데이터 파일이 손상되었습니다. 기본 데이터로 복구합니다.")
        return default_quizzes

def main():
    try:
        quizzes = load_data()
        
        while True:
            print("\n=== 퀴즈 프로그램 ===")
            print("1. 퀴즈 풀기")
            print("2. 종료")
            
            choice = get_safe_input("메뉴를 선택하세요: ", 1, 2)
            
            if choice == 1:
                for i, q in enumerate(quizzes, 1):
                    q.display(i)
                    user_ans = get_safe_input("정답 번호를 입력하세요 (1-4): ", 1, 4)
                    if q.is_correct(user_ans):
                        print("정답입니다! ✨")
                    else:
                        print(f"틀렸습니다. 정답은 {q.answer}번입니다. 😢")
            elif choice == 2:
                print("프로그램을 종료합니다.")
                break

    except (KeyboardInterrupt, EOFError):
        print("\n\n[알림] 사용자에 의해 프로그램이 중단되었습니다. 안전하게 종료합니다.")
        # 필요한 경우 여기서 저장 로직 호출

if __name__ == "__main__":
    main()