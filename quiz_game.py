from default_quizzes import create_default_quizzes

class QuizGame:
    def __init__(self):
        self.quizzes = create_default_quizzes()
        self.best_score = 0

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
            print("🎉 새로운 최고 점수입니다!")
            self.best_score = score
        print()

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
