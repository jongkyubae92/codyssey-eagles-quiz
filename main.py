import random
import json
import os

class Quiz:
    def __init__(self, question, choices, answer, hint):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.hint = hint

    def display(self, index):
        print(f"\n문제 {index}: {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint
        }

class QuizGame:
    def __init__(self):
        self.state_file = "state.json"
        self.quizzes = []
        self.best_score = 0.0
        self.load_state()

    def get_default_quizzes(self):
        """기본 퀴즈 데이터 (파일이 없을 때 사용)"""
        return [
            Quiz("한화이글스가 KBO 리그에 처음 참가한 연도는?", ["1985년", "1987년", "1984년", "1986년"], 4, "빙그레 이글스의 시작"),
            Quiz("한화이글스가 한국시리즈에서 처음 우승한 해는?", ["1998년", "1996년", "2001년", "1999년"], 4, "세기말"),
            Quiz("KBO 통산 최다승 투수는?", ["송진우", "정민철", "류현진", "구대성"], 1, "세광고 출신"),
            Quiz("한화이글스의 연고지는?", ["대전", "대구", "서울", "부산"], 1, "교통의 요지"),
            Quiz("류현진 선수의 등번호는?", ["0", "1", "99", "100"], 3, "모르면 간첩"),
        ]

    def load_state(self):
        if not os.path.exists(self.state_file):
            self.quizzes = self.get_default_quizzes()
            self.save_state()
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_score = float(data.get("best_score", 0.0))
                quiz_data = data.get("quizzes", [])
                
                if not quiz_data:
                    self.quizzes = self.get_default_quizzes()
                else:
                    # 1. 기본 퀴즈의 힌트들을 딕셔너리 형태로 미리 준비합니다.
                    default_hints = {q.question: q.hint for q in self.get_default_quizzes()}
                    
                    new_quizzes = []
                    for q in quiz_data:
                        # 2. 파일에서 가져온 힌트가 없거나 '힌트 없음'일 경우
                        current_hint = q.get('hint', '힌트 없음')
                        if current_hint == '힌트 없음':
                            # 기본 힌트 딕셔너리에서 질문 내용을 찾아 힌트를 가져옵니다.
                            current_hint = default_hints.get(q['question'], '힌트 정보가 없습니다.')
                        
                        new_quizzes.append(Quiz(q['question'], q['choices'], q['answer'], current_hint))
                    
                    self.quizzes = new_quizzes
                    
                    # 3. 힌트가 채워진 데이터를 파일에 다시 저장하여 업데이트합니다.
                    self.save_state()

        except (json.JSONDecodeError, KeyError, IOError):
            print("\n[알림] 데이터 파일이 손상되어 기본 데이터를 로드합니다.")
            self.quizzes = self.get_default_quizzes()

    def save_state(self):
        try:
            state_data = {
                "best_score": self.best_score,
                "quizzes": [q.to_dict() for q in self.quizzes]
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"\n[오류] 저장 실패: {e}")

    def get_safe_input(self, prompt, min_val, max_val):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input: continue
                val = int(user_input)
                if min_val <= val <= max_val: return val
                print(f">> {min_val}~{max_val} 사이의 숫자를 입력하세요.")
            except ValueError:
                print(">> 숫자를 입력해 주세요.")
            except (EOFError, KeyboardInterrupt):
                return None

    def get_non_empty_input(self, prompt):
        while True:
            val = input(prompt).strip()
            if val: return val
            print(">> 내용을 입력해 주세요.")

    def play(self):
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return

        total_available = len(self.quizzes)
        num_to_solve = self.get_safe_input(f"\n몇 문제를 풀겠습니까? (1~{total_available}): ", 1, total_available)
        if num_to_solve is None: return

        quiz_pool = self.quizzes[:]
        random.shuffle(quiz_pool)
        quiz_pool = quiz_pool[:num_to_solve]

        score = 0.0
        print(f"\n--- 퀴즈 시작! (힌트 사용 시 해당 문제 0.5점) ---")
        
        for i, q in enumerate(quiz_pool, 1):
            hint_used = False
            q.display(i)
            
            while True:
                ans = self.get_safe_input("정답 번호 입력 (힌트보기: 0): ", 0, 4)
                if ans is None: return
                
                if ans == 0:
                    print(f"💡 힌트: {q.hint}")
                    hint_used = True
                    continue # 다시 정답 입력을 기다림
                break

            if q.is_correct(ans):
                points = 0.5 if hint_used else 1.0
                print(f"정답입니다! (+{points}점) ✨")
                score += points
            else:
                print(f"오답입니다. 정답은 {q.answer}번입니다. 😢")

        print("\n" + "="*30)
        print(f"이번 점수: {score} / {num_to_solve}")
        if score > self.best_score:
            print(f"🎊 최고 기록 경신! ({self.best_score} -> {score})")
            self.best_score = score
            self.save_state()
        else:
            print(f"현재 최고 기록: {self.best_score}점")
        print("="*30)

    def add(self):
        """끊겼던 퀴즈 추가 기능 완성"""
        print("\n--- 새 퀴즈 추가 ---")
        question = self.get_non_empty_input("문제 내용: ")
        choices = []
        for i in range(1, 5):
            choices.append(self.get_non_empty_input(f"선택지 {i}: "))
        answer = self.get_safe_input("정답 번호 (1-4): ", 1, 4)
        hint = self.get_non_empty_input("힌트 내용: ")
        
        if answer:
            self.quizzes.append(Quiz(question, choices, answer, hint))
            self.save_state()
            print("\n[성공] 새로운 퀴즈가 등록되었습니다!")

    def list_all(self):
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return
        print(f"\n--- 등록된 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question} (정답: {q.answer}번)")

    def show_score(self):
        print("\n" + "="*30)
        print(f"🏆 현재 최고 기록: {self.best_score}점")
        print("="*30)

if __name__ == "__main__":
    game = QuizGame()
    while True:
        print("\n[한화이글스 퀴즈 프로그램]")
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 추가")
        print("3. 퀴즈 목록")
        print("4. 최고 기록")
        print("5. 종료")
        
        choice = game.get_safe_input("메뉴 선택: ", 1, 5)
        if choice == 1: game.play()
        elif choice == 2: game.add()
        elif choice == 3: game.list_all()
        elif choice == 4: game.show_score()
        elif choice == 5 or choice is None:
            print("프로그램을 종료합니다. 최강한화! 🦅")
            break