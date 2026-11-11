import random
import shutil
import json
import os
from datetime import datetime

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
        self.history = []
        self.best_score = 0.0
        # 데이터를 로드하고, 실패 시 기본 퀴즈로 초기화
        self.initialize_data()

    def get_default_quizzes(self):
        return [
            Quiz("한화이글스가 KBO 리그에 처음 참가한 연도는?", ["1985년", "1987년", "1984년", "1986년"], 4, "빙그레 이글스의 시작"),
            Quiz("한화이글스가 한국시리즈에서 처음 우승한 해는?", ["1998년", "1996년", "2001년", "1999년"], 4, "세기말"),
            Quiz("KBO 통산 최다승 투수는?", ["송진우", "정민철", "류현진", "구대성"], 1, "세광고 출신"),
            Quiz("한화이글스의 연고지는?", ["대전", "대구", "서울", "부산"], 1, "교통의 요지"),
            Quiz("류현진 선수의 등번호는?", ["0", "1", "99", "100"], 3, "모르면 간첩"),
        ]

    def save_state(self):
        """현재 상태를 저장하고 백업본(.bak)을 생성합니다."""
        try:
            # 1. 기존 파일 백업
            if os.path.exists(self.state_file):
                shutil.copy(self.state_file, f"{self.state_file}.bak")
            
            # 2. 데이터 저장
            state_data = {
                "best_score": self.best_score,
                "history": self.history,
                "quizzes": [q.to_dict() for q in self.quizzes]
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(state_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"\n[오류] 데이터 저장 실패: {e}")

    def load_state(self):
        """파일에서 데이터를 읽어옵니다. 손상 시 백업본을 시도합니다."""
        target_files = [self.state_file, f"{self.state_file}.bak"]
        
        for file_path in target_files:
            if os.path.exists(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except (json.JSONDecodeError, IOError):
                    print(f"⚠️ {file_path} 파일이 손상되었습니다.")
                    continue
        return None

    def initialize_data(self):
        """로드된 데이터를 바탕으로 객체를 초기화합니다."""
        data = self.load_state()
        if data:
            self.best_score = data.get("best_score", 0.0)
            self.history = data.get("history", [])
            # 딕셔너리 리스트를 Quiz 객체 리스트로 변환
            self.quizzes = [Quiz(**q) for q in data.get("quizzes", [])]
            if not self.quizzes:
                self.quizzes = self.get_default_quizzes()
        else:
            print(">> 데이터를 찾을 수 없어 기본값으로 시작합니다.")
            self.quizzes = self.get_default_quizzes()

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

    def play(self):
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return
        
        total_available = len(self.quizzes)
        num_to_solve = self.get_safe_input(f"\n몇 문제를 풀겠습니까? (1~{total_available}): ", 1, total_available)
        if num_to_solve is None: return

        quiz_pool = random.sample(self.quizzes, num_to_solve)
        score = 0.0

        for i, q in enumerate(quiz_pool, 1):
            hint_used = False
            q.display(i)
            while True:
                ans = self.get_safe_input("정답 번호 입력 (힌트보기: 0): ", 0, 4)
                if ans is None: return
                if ans == 0:
                    print(f"💡 힌트: {q.hint}")
                    hint_used = True
                    continue
                break
            
            if q.is_correct(ans):
                points = 0.5 if hint_used else 1.0
                print(f"정답입니다! (+{points}점) ✨")
                score += points
            else:
                print(f"오답입니다. 정답은 {q.answer}번입니다. 😢")

        # 결과 저장 로직 (예시)
        print(f"\n총점: {score} / {float(num_to_solve)}")
        if score > self.best_score:
            self.best_score = score
            print("🎉 최고 기록 경신!")
        
        self.history.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total": num_to_solve,  # 이 부분을 추가해서 총 문제 수를 저장합니다!
            "score": score
        })
        self.save_state()

    def show_history(self):
        if not self.history:
            print("\n[알림] 아직 게임 기록이 없습니다.")
            return

        print("\n" + "="*45)
        print(f"{'날짜 및 시간':^19} | {'문제 수':^5} | {'점수':^5}")
        print("-" * 45)
        
        for h in self.history:
            # .get()을 사용하면 키가 없어도 에러 대신 기본값(N/A)을 보여줍니다.
            date = h.get('date', 'Unknown')
            total = h.get('total', '-') 
            score = h.get('score', 0.0)
            print(f"{date} | {total:^7} | {score:^7}")
        print("="*45)

    def add(self):
        print("\n--- 새 퀴즈 추가 ---")
        question = input("문제 내용: ").strip()
        choices = [input(f"선택지 {i}: ").strip() for i in range(1, 5)]
        answer = self.get_safe_input("정답 번호 (1-4): ", 1, 4)
        hint = input("힌트 내용: ").strip()
        if answer:
            self.quizzes.append(Quiz(question, choices, answer, hint))
            self.save_state()
            print("\n[성공] 퀴즈가 추가되었습니다!")

    def list_all(self):
        if not self.quizzes:
            print("\n[알림] 등록된 퀴즈가 없습니다.")
            return
        print(f"\n--- 등록된 퀴즈 목록 (총 {len(self.quizzes)}개) ---")
        for i, q in enumerate(self.quizzes, 1):
            print(f"{i}. {q.question}")

    def delete(self):
        if not self.quizzes: return
        self.list_all()
        target_idx = self.get_safe_input(f"\n삭제할 번호 (취소: 0): ", 0, len(self.quizzes))
        if target_idx == 0 or target_idx is None: return
        removed = self.quizzes.pop(target_idx - 1)
        self.save_state()
        print(f"\n[삭제 완료] '{removed.question}'")

if __name__ == "__main__":
    game = QuizGame()
    while True:
        print("\n1.풀기 2.추가 3.목록 4.삭제 5.기록보기 6.종료")
        choice = game.get_safe_input("선택: ", 1, 6)
        if choice == 1: game.play()
        elif choice == 2: game.add()
        elif choice == 3: game.list_all()
        elif choice == 4: game.delete()
        elif choice == 5: game.show_history()
        elif choice == 6 or choice is None: break