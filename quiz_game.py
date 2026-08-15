import json
from pathlib import Path
import random
from datetime import datetime

from default_quizzes import create_default_quizzes
from quiz import Quiz

STATE_FILE = Path(__file__).resolve().parent / "state.json"
class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None
        self.score_history = []
        self.load_state()

    def run(self):
        while True:
            self.show_menu()
            choice = self._get_valid_number("선택: ", 1, 7)
            if choice == 1:
                self.play_quiz()
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.show_quizzes()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.delete_quiz()
            elif choice == 6:
                 self.show_score_history()
            elif choice == 7:
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
5. 퀴즈 삭제
6. 점수 기록
7. 종료
========================================"""
            )

    def play_quiz(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return
        question_count = self._get_valid_number(
            f"풀 문제 수를 입력하세요 (1~{len(self.quizzes)}): ", 1, len(self.quizzes))

        quiz_list = self.quizzes.copy()
        random.shuffle(quiz_list)
        quiz_list = quiz_list[:question_count]

        correct_count = 0
        hint_count = 0
        total_count = len(quiz_list)

        print(f"\n📝 퀴즈를 시작합니다! (총 {total_count}문제)")

        for idx, quiz in enumerate(quiz_list):
            print("\n----------------------------------------")
            print(f"문제 [{idx + 1}]") 
            quiz.display()

            use_hint = self._get_yes_or_no("힌트를 사용하시겠습니까? (y/n): ")

            if use_hint:
                quiz.show_hint()
                hint_count += 1

            user_answer = self._get_valid_number("정답 입력: ", 1, 4)

            if quiz.is_correct(user_answer):
                print("✅ 정답입니다!")
                correct_count += 1
            else:
                print("오답입니다!")

        score = int(100 * correct_count / total_count)
        penalty = hint_count * 10
        score = max(0, score - penalty)
        record = {
            "played_at": datetime.now().isoformat(timespec="seconds"),
            "question_count": total_count,
            "score": score,
        }
        self.score_history.append(record)

        is_new_best = (
            self.best_score is None
            or score > self.best_score
        )

        if is_new_best:
            self.best_score = score

        self.save_state()

        print("\n========================================")
        print(f"🏆 결과: {total_count}문제 중 {correct_count}문제 정답! ({score}점)")

        if hint_count:
            print(f"힌트 사용: {hint_count}회 (-{penalty}점)")

        if is_new_best:
            print("🎉 새로운 최고 점수입니다!")

        print()

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")
        question = self._get_valid_input("문제를 입력하세요: ")

        choices = []
        for i in range(1, 5):
            choices.append(self._get_valid_input(f"선택지 {i}: "))

        answer = self._get_valid_number("정답 번호 (1-4): ", 1, 4)

        hint = self._get_valid_input("힌트를 입력하세요: ")

        self.quizzes.append(Quiz(question, choices, answer, hint))
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
        if self.best_score is None:
            print("아직 문제를 푼 기록이 없습니다.")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")

    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quizzes],
            "best_score": self.best_score,
            "score_history": self.score_history,
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

            if not isinstance(data, dict):
                raise ValueError
            
            quizzes_data = data["quizzes"]
            best_score = data["best_score"]
            score_history = data.get("score_history", [])
            
            if not isinstance(quizzes_data, list):
                raise ValueError

            if best_score is not None:
                if type(best_score) is not int or not 0 <= best_score <= 100:
                    raise ValueError
                
            if not isinstance(score_history, list):
                raise ValueError

            for record in score_history:
                if not isinstance(record, dict):
                    raise ValueError

                played_at = record["played_at"]
                question_count = record["question_count"]
                score = record["score"]

                if not isinstance(played_at, str):
                    raise ValueError

                datetime.fromisoformat(played_at)

                if type(question_count) is not int or question_count < 1:
                    raise ValueError

                if type(score) is not int or not 0 <= score <= 100:
                    raise ValueError
            
            quizzes = [
                Quiz.from_dict(quiz_data)
                for quiz_data in quizzes_data
            ]

            self.quizzes = quizzes
            self.best_score = best_score
            self.score_history = score_history

            if self.best_score is None:
                score_message = "플레이 기록 없음"
            else:
                score_message = f"최고 점수 {self.best_score}점"

            print(
                f"저장된 데이터를 불러왔습니다. "
                f"(퀴즈 {len(self.quizzes)}개, {score_message})"
            )

        except FileNotFoundError:
            print("저장된 데이터가 없어 기본 퀴즈를 사용합니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일이 손상되어 기본 퀴즈를 사용합니다.")

        except OSError as error:
            print(f"데이터를 불러오지 못해 기본 퀴즈를 사용합니다: {error}")
        
    def delete_quiz(self):
        if not self.quizzes:
            print("삭제할 퀴즈가 없습니다.")
            return

        self.show_quizzes()

        quiz_number = self._get_valid_number(
            f"삭제할 퀴즈 번호를 입력하세요 (1~{len(self.quizzes)}): ", 1, len(self.quizzes))

        quiz = self.quizzes[quiz_number - 1]

        confirm = self._get_yes_or_no(
            f"'{quiz.question}' 퀴즈를 삭제하시겠습니까? (y/n): "
        )

        if not confirm:
            print("퀴즈 삭제를 취소했습니다.")
            return

        deleted_quiz = self.quizzes.pop(quiz_number - 1)
        self.save_state()

        print(f"✅ '{deleted_quiz.question}' 퀴즈가 삭제되었습니다.")

    def show_score_history(self):
        if not self.score_history:
            print("아직 저장된 게임 기록이 없습니다.")
            return

        print("\n📊 점수 기록")
        print("----------------------------------------")

        for idx, record in enumerate(self.score_history, start=1):
            print(
                f"[{idx}] {record['played_at']} | "
                f"{record['question_count']}문제 | "
                f"{record['score']}점"
            )

        print("----------------------------------------")


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

    def _get_yes_or_no(self, prompt):
        while True:
            value = input(prompt).strip().lower()

            if value == "y":
                return True

            if value == "n":
                return False

            print("y 또는 n을 입력해 주세요.")