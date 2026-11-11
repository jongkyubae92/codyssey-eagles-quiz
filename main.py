import random
import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index):
        """문제를 화면에 출력합니다."""
        print(f"\n문제 {index}: {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        """정답 여부를 확인합니다."""
        return user_answer == self.answer

    def to_dict(self):
        """객체를 딕셔너리로 변환 (저장용)"""
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer
        }

class QuizGame:
    def __init__(self):
        self.state_file = "state.json"
        self.quizzes = []
        self.best_score = 0
        self.load_state() # 초기화 시 데이터 로드

    def get_default_quizzes(self):
        """기본 퀴즈 데이터 반환"""
        return [
            Quiz("한화이글스가 KBO 리그에 처음 참가한 연도는?", ["1985년", "1987년", "1984년", "1986년"], 4),
            Quiz("한화이글스가 한국시리즈에서 처음 우승한 해는?", ["1998년", "1996년", "2001년", "1999년"], 4),
            Quiz("KBO 통산 최다승 투수는?", ["송진우", "정민철", "류현진", "구대성"], 1),
            Quiz("한화이글스의 연고지는?", ["대전", "대구", "서울", "부산"], 1),
            Quiz("류현진 선수의 등번호는?", ["0", "1", "99", "100"], 3),
        ]

    def load_state(self):
        """state.json에서 모든 데이터를 불러옵니다."""
        if not os.path.exists(self.state_file):
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0
            return

        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.best_score = data.get("best_score", 0)
                quiz_data = data.get("quizzes", [])
                
                if not quiz_data:
                    self.quizzes = self.get_default_quizzes()
                else:
                    self.quizzes = [Quiz(q['question'], q['choices'], q['answer']) for q in quiz_data]
        except (json.JSONDecodeError, KeyError, IOError):
            print("\n[알림] 데이터 파일이 손상되어 기본 데이터를 로드합니다.")
            self.quizzes = self.get_default_quizzes()
            self.best_score = 0

    def save_state(self):
        """현재 상태를 state.json에 저장합니다."""
        try:
            state_data = {
                "best_score": self.best_score,
                "quizzes": [q.to_dict() for q in self.quizzes]
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"\n[오류] 저장 실패: {e}")

    # --- 유틸리티 메서드 ---
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

        # 1. 문제 수 선택받기
        total_available = len(self.quizzes)
        print(f"\n현재 총 {total_available}개의 문제가 준비되어 있습니다.")
        num_to_solve = self.get_safe_input(f"몇 문제를 풀겠습니까? (1~{total_available}): ", 1, total_available)
        
        if num_to_solve is None: return # 중도 종료(Ctrl+C 등) 처리

        # 2. 퀴즈 섞기 및 선택한 수만큼 자르기
        quiz_pool = self.quizzes[:]
        random.shuffle(quiz_pool)
        quiz_pool = quiz_pool[:num_to_solve] # 사용자가 선택한 개수만큼만 슬라이싱

        score = 0
        print(f"\n--- 퀴즈 시작! (총 {num_to_solve}문제) ---")
        
        for i, q in enumerate(quiz_pool, 1):
            q.display(i)
            ans = self.get_safe_input("정답 번호 입력: ", 1, 4)
            if ans is None: return
            
            if q.is_correct(ans):
                print("정답입니다! ✨")
                score += 1
            else:
                print(f"오답입니다. 정답은 {q.answer}번입니다. 😢")

        # 3. 결과 출력 (선택한 문제 수 기준으로 점수 계산)
        print("\n" + "="*30)
        print(f"이번 점수: {score} / {num_to_solve}")
        
        # 최고 기록은 '개수'로 저장할지, '비율'로 저장할지 결정해야 합니다.
        # 여기서는 단순히 맞춘 문제 수(score)로 비교하겠습니다.
        if score > self.best_score:
            print(f"🎊 최고 기록 경신! ({self.best_score} -> {score})")
            self.best_score = score
            self.save_state()
        else:
            print(f"현재 최고 기록: {self.best_score}점")
        print("="*30)

    def add(self):
        print("\n--- 새 퀴즈 추가 ---")
        question = self.get_non_empty_input("문제 내용: ")
        choices = [self.get_non_empty_input(f"선택지 {i}: ") for i in range(1, 5)]
        answer = self.get_safe_input("정답 번호 (1-4): ", 1, 4)
        
        if answer:
            self.quizzes.append(Quiz(question, choices, answer))
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
        """최고 기록을 출력합니다."""
        print("\n" + "="*30)
        if self.best_score == 0:
            print("아직 기록이 없습니다. 첫 게임에 도전하세요!")
        else:
            print(f"🏆 현재 최고 기록은 {self.best_score}점입니다.")
        print("="*30)

    def run(self):
        menu_map = {
            '1': self.play,
            '2': self.add,
            '3': self.list_all,
            '4': self.show_score
        }
        
        while True:
            print("\n--- 한화이글스 퀴즈 프로그램 ---")
            print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 목록 보기  4. 최고 점수  5. 종료")
            choice = input("메뉴 선택: ").strip()
            
            if choice == '5':
                print("프로그램을 종료합니다. 🦅")
                break
            elif choice in menu_map:
                menu_map[choice]()
            else:
                print("잘못된 선택입니다. 다시 선택해 주세요.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()