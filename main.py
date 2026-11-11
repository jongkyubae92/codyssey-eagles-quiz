import json
import os

class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self, index):
        print(f"\n문제 {index}: {self.question}")
        for i, choice in enumerate(self.choices, 1):
            print(f"  {i}. {choice}")

    def is_correct(self, user_answer):
        return user_answer == self.answer

class QuizGame:
    def __init__(self):
        self.quiz_file = "quizzes.json"
        self.score_file = "score.json"
        self.quizzes = self._load_quizzes()
        self.high_score = self._load_high_score()

    # --- 파일 입출력 (내부 메서드) ---
    def _load_quizzes(self):
        default_quizzes = [
            Quiz("한화이글스가 KBO 리그에 처음 참가한 연도는?", ["1985년", "1987년", "1984년", "1986년"], 4),
            Quiz("한화이글스가 한국시리즈에서 처음 우승한 해는?", ["1998년", "1996년", "2001년", "1999년"], 4),
            Quiz("KBO 통산 최다승 투수는?", ["송진우", "정민철", "류현진", "구대성"], 1),
            Quiz("한화이글스의 연고지는?", ["대전", "대구", "서울", "부산"], 1),
            Quiz("류현진 선수의 등번호는?", ["0", "1", "99", "100"], 3),
        ]
        if not os.path.exists(self.quiz_file):
            return default_quizzes
        try:
            with open(self.quiz_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Quiz(q['question'], q['choices'], q['answer']) for q in data]
        except:
            return default_quizzes

    def _save_quizzes(self):
        data = [{"question": q.question, "choices": q.choices, "answer": q.answer} for q in self.quizzes]
        with open(self.quiz_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def _load_high_score(self):
        if not os.path.exists(self.score_file):
            return 0
        try:
            with open(self.score_file, "r", encoding="utf-8") as f:
                return json.load(f).get("high_score", 0)
        except:
            return 0

    def _save_high_score(self, score):
        with open(self.score_file, "w", encoding="utf-8") as f:
            json.dump({"high_score": score}, f)
        self.high_score = score

    # --- 유틸리티 메서드 ---
    @staticmethod
    def get_safe_input(prompt, min_val, max_val):
        while True:
            try:
                user_input = input(prompt).strip()
                if not user_input: continue
                val = int(user_input)
                if min_val <= val <= max_val: return val
                print(f">> {min_val}~{max_val} 사이를 입력하세요.")
            except ValueError:
                print(">> 숫자를 입력하세요.")
            except (EOFError, KeyboardInterrupt):
                return None

    # --- 주요 기능 메서드 ---
    def play(self):
        if not self.quizzes:
            print("\n[알림] 퀴즈가 없습니다.")
            return

        score = 0
        print(f"\n--- 퀴즈 시작! (총 {len(self.quizzes)}문제) ---")
        for i, q in enumerate(self.quizzes, 1):
            q.display(i)
            choice = self.get_safe_input("정답 번호: ", 1, 4)
            if choice is None: return
            
            if q.is_correct(choice):
                print("정답! ✨")
                score += 1
            else:
                print(f"오답! 정답은 {q.answer}번입니다.")

        print(f"\n결과: {score}/{len(self.quizzes)}")
        if score > self.high_score:
            print(f"🎊 최고 기록 경신! ({self.high_score} -> {score})")
            self._save_high_score(score)
        else:
            print(f"최고 기록: {self.high_score}")

    def add(self):
        print("\n--- 새 퀴즈 추가 ---")
        q_text = input("문제 내용: ").strip()
        if not q_text: return
        choices = [input(f"선택지 {i}: ").strip() for i in range(1, 5)]
        answer = self.get_safe_input("정답 번호 (1-4): ", 1, 4)
        
        if answer:
            self.quizzes.append(Quiz(q_text, choices, answer))
            self._save_quizzes()
            print("[성공] 추가되었습니다.")

    def list_all(self):
        print(f"\n--- 퀴즈 목록 ({len(self.quizzes)}개) ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def show_score(self):
        print(f"\n🏆 현재 최고 점수: {self.high_score}점")

    def run(self):
        """메인 메뉴 루프"""
        menu_map = {
            '1': self.play,
            '2': self.add,
            '3': self.list_all,
            '4': self.show_score
        }
        
        while True:
            print("\n--- 한화이글스 퀴즈 게임 (Class Ver.) ---")
            print("1. 퀴즈 풀기  2. 퀴즈 추가  3. 목록 보기  4. 최고 점수  5. 종료")
            choice = input("선택: ").strip()
            
            if choice == '5':
                print("종료합니다. 🦅")
                break
            elif choice in menu_map:
                menu_map[choice]()
            else:
                print("잘못된 선택입니다.")

if __name__ == "__main__":
    game = QuizGame()
    game.run()