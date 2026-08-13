class Quiz:
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer

    def display(self):
        print(self.question)
        print()
        for idx, choice in enumerate(self.choices):
            print(f"{idx + 1}. {choice}")

    def is_correct(self, user_answer):
        return self.answer == user_answer