import json
from pathlib import Path

from default_quizzes import create_default_quizzes
from quiz import Quiz

STATE_FILE = Path(__file__).resolve().parent / "state.json"
class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = 0
        self.load_state()

    def run(self):
        while True:
            self.show_menu()
            choice = self._get_valid_number("선택: ", 1, 5)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                print("게임을 종료합니다.")
                break


    def show_menu(self):
        print(
"""========================================
    🎯 나만의 퀴즈 게임 🎯
========================================
1. 퀴즈 풀기
2. 퀴즈 추가
3. 퀴즈 목록
4. 점수 확인
5. 종료
========================================"""
            )

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        
        correct_count = 0
        total_count = len(self.quizzes)

        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

        for idx, quiz in enumerate(self.quizzes):
            print("\n----------------------------------------")
            print(f"문제 [{idx + 1}]") 
            quiz.display()

            user_answer = self._get_valid_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print("오답입니다!")

        score = int(100 * correct_count / total_count)
        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")
        if score > self.best_score:
            self.best_score = score
            self.save_state()
            print("🎉 새로운 최고 점수입니다!")
            
        print()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self._get_valid_input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choices.append(self._get_valid_input(f"선택지 {i}: "))

        answer = self._get_valid_number("정답 번호 (1-4): ", 1, 4)

        self.quizzes.append(Quiz(question, choices, answer))
        self.save_state()
        print("\n✅ 퀴즈가 추가되었습니다!")

    def show_quizzes(self):
        if not len(self.quizzes):
            print("\n등록된 퀴즈가 없습니다.")
            return
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print("----------------------------------------")
        for idx, quiz in enumerate(self.quizzes):
            print(f"[{idx+1}] {quiz.question}")
        print("----------------------------------------")

    def show_best_score(self):
        pass

    def save_state(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer,
                }
                for quiz in self.quizzes
            ],
            "best_score": self.best_score,
        }
        try:
            with open(STATE_FILE, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except OSError as error:
            print(f"데이터를 저장하지 못했습니다: {error}")


    def load_state(self):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = [
                Quiz(
                    quiz_data["question"],
                    quiz_data["choices"],
                    quiz_data["answer"],
                )
                for quiz_data in data["quizzes"]
            ]

            best_score = data["best_score"]

            self.quizzes = quizzes
            self.best_score = best_score

            print(
                f"저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, 최고 점수 {self.best_score}점)"
            )

        except FileNotFoundError:
            print("저장된 데이터가 없어 기본 퀴즈를 사용합니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일이 손상되어 기본 퀴즈를 사용합니다.")

        except OSError as error:
            print(f"데이터를 불러오지 못해 기본 퀴즈를 사용합니다: {error}")
        

    def _get_valid_number(self, prompt, minimum, maximum):
        while True:
            value = input(prompt).strip()

            if not value:
                print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")
                continue

            try:
                number = int(value)
            except ValueError:
                print(f"{minimum}~{maximum} 사이의 숫자를 입력해 주세요.")
                continue

            if not minimum <= number <= maximum:
                print(f"{minimum}~{maximum} 사이의 숫자를 입력해 주세요.")
                continue

            return number

    def _get_valid_input(self, prompt):
        while True:
            user_input = input(prompt).strip()
            if user_input:
                return user_input
            print("빈 값은 입력할 수 없습니다. 다시 입력해주세요.")

