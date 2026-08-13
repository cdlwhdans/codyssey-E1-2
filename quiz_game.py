from default_quizzes import create_default_quizzes
class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = None

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
        pass

    def add_quiz(self):
        pass

    def show_quizzes(self):
        pass

    def show_best_score(self):
        pass

    def save_state(self):
        pass

    def load_state(self):
        pass

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
