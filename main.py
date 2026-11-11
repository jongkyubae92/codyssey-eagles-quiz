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

# --- 점수 관련 함수 추가 ---
def load_high_score():
    """파일에서 최고 점수를 불러옵니다."""
    file_path = "score.json"
    if not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("high_score", 0)
    except (json.JSONDecodeError, KeyError):
        return 0

def save_high_score(score):
    """최고 점수를 파일에 저장합니다."""
    file_path = "score.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"high_score": score}, f)

# --- 입력 및 데이터 관리 함수 ---
def get_safe_input(prompt, min_val, max_val):
    """안전한 숫자 입력 함수"""
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
            return None

def load_data():
    """퀴즈 데이터 로드"""
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

def save_data(quizzes):
    """퀴즈 데이터를 JSON 파일로 저장"""
    file_path = "quizzes.json"
    data = [{"question": q.question, "choices": q.choices, "answer": q.answer} for q in quizzes]
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_non_empty_input(prompt):
    """비어 있지 않은 문자열 입력"""
    while True:
        val = input(prompt).strip()
        if val: return val
        print(">> [오류] 내용을 입력해 주세요.")

# --- 메뉴 기능 함수 ---
def play_quiz(quizzes):
    if not quizzes:
        print("\n[알림] 등록된 퀴즈가 없습니다.")
        return

    score = 0
    total = len(quizzes)
    print(f"\n--- 퀴즈 시작! (총 {total}문제) ---")

    for i, q in enumerate(quizzes, 1):
        q.display(i)
        choice = get_safe_input("정답 번호 입력: ", 1, 4)
        if choice is None: return
        
        if q.is_correct(choice):
            print("정답입니다! ✨")
            score += 1
        else:
            print(f"오답입니다. 정답은 {q.answer}번입니다. 😢")

    print("\n" + "="*30)
    print(f"이번 점수: {score} / {total}")
    
    high_score = load_high_score()
    if score > high_score:
        print(f"🎊 축하합니다! 최고 기록 경신! ({high_score} -> {score})")
        save_high_score(score)
    else:
        print(f"현재 최고 기록: {high_score}점")
    print("="*30)

def add_quiz(quizzes):
    print("\n--- 새 퀴즈 추가 ---")
    question = get_non_empty_input("문제 내용: ")
    choices = [get_non_empty_input(f"선택지 {i}: ") for i in range(1, 5)]
    answer = get_safe_input("정답 번호 (1-4): ", 1, 4)
    
    if answer:
        quizzes.append(Quiz(question, choices, answer))
        save_data(quizzes)
        print("\n[성공] 새로운 퀴즈가 등록되었습니다!")

def list_quizzes(quizzes):
    if not quizzes:
        print("\n[알림] 등록된 퀴즈가 없습니다.")
        return
    print(f"\n--- 퀴즈 목록 (총 {len(quizzes)}개) ---")
    for i, q in enumerate(quizzes, 1):
        print(f"{i}. {q.question} (정답: {q.answer}번)")

def show_high_score():
    high_score = load_high_score()
    if high_score == 0:
        print("\n[알림] 아직 도전 기록이 없습니다.")
    else:
        print(f"\n🏆 현재 최고 점수: {high_score}점")

# --- 메인 루프 ---
def main():
    quizzes = load_data()
    while True:
        print("\n--- 한화이글스 퀴즈 프로그램 ---")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 점수 확인")
        print("5. 종료")
        
        menu = input("메뉴 선택: ").strip()
        
        if menu == '1':
            play_quiz(quizzes)
        elif menu == '2':
            add_quiz(quizzes)
        elif menu == '3':
            list_quizzes(quizzes)
        elif menu == '4':
            show_high_score()
        elif menu == '5':
            print("프로그램을 종료합니다. 🦅")
            break
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()