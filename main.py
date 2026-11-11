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
    """안전한 입력 함수"""
    while True:
        try:
            user_input = input(prompt).strip()
            if not user_input:
                print(">> [오류] 입력값이 비어 있습니다.")
                continue
            val = int(user_input)
            if min_val <= val <= max_val:
                return val
            else:
                print(f">> [오류] {min_val}에서 {max_val} 사이의 숫자를 입력해 주세요.")
        except ValueError:
            print(">> [오류] 숫자가 아닌 값이 입력되었습니다.")
        except (EOFError, KeyboardInterrupt):
            return None # 중단 시 None 반환

def load_data():
    """데이터 로드 함수"""
    default_quizzes = [
        Quiz("한화이글스가 KBO 리그에 처음 참가한 연도는 언제일까요?", ["1985년", "1987년", "1984년", "1986년"], 4),
        Quiz("한화이글스가 한국시리즈에서 처음 우승한 해는 언제일까요?", ["1998년", "1996년", "2001년", "1999년"], 4),
        Quiz("한화이글스의 대표적인 레전드 투수이자 KBO 통산 최다승 기록을 보유한 선수는 누구일까요?", ["송진우", "정민철", "류현진", "구대성"], 1),
        Quiz("한화이글스의 연고지는 어디일까요?", ["대전광역시", "대구광역시", "서울특별시", "부산광역시"], 1),
        Quiz("류현진 선수의 등번호는 몇 번일까요?", ["0", "1", "99", "100"], 3),
    ]
    
    file_path = "quizzes.json"
    if not os.path.exists(file_path):
        return default_quizzes

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Quiz(q['question'], q['choices'], q['answer']) for q in data]
    except (json.JSONDecodeError, KeyError):
        return default_quizzes

def play_quiz(quizzes):
    """퀴즈 풀기 기능"""
    if not quizzes:
        print("\n[알림] 등록된 퀴즈가 없습니다.")
        return

    score = 0
    total = len(quizzes)

    print(f"\n--- 퀴즈를 시작합니다! (총 {total}문제) ---")

    for i, q in enumerate(quizzes, 1):
        # 1. 클래스 내부의 display 메서드 활용
        q.display(i)

        # 2. 기존에 만든 get_safe_input 함수 활용 (코드 간결화)
        choice = get_safe_input("정답 번호 입력: ", 1, 4)
        
        if choice is None: # 사용자가 강제 종료했을 때
            print("\n[알림] 퀴즈를 중단합니다.")
            return

        # 3. 클래스 내부의 is_correct 메서드 활용
        if q.is_correct(choice):
            print("정답입니다! ✨")
            score += 1
        else:
            print(f"오답입니다. 정답은 {q.answer}번입니다. 😢")

    print("\n" + "="*30)
    print(f"최종 점수: {score} / {total}")
    print(f"정답률: {(score/total)*100:.1f}%")
    print("="*30)

def main():
    quizzes = load_data()
    
    while True:
        print("\n--- 한화이글스 퀴즈 프로그램 ---")
        print("1. 퀴즈 풀기")
        print("2. 종료")
        
        menu = input("메뉴 선택: ").strip()
        
        if menu == '1':
            play_quiz(quizzes)
        elif menu == '2':
            print("프로그램을 종료합니다. 보살 팬 여러분 화이팅! 🦅")
            break
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()