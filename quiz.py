class Quiz:
    def __init__(
        self,
        question,
        choices,
        answer,
        hint="등록된 힌트가 없습니다.",
    ):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 빈 문자열일 수 없습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 4개여야 합니다.")

        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("선택지는 빈 문자열일 수 없습니다.")

        if type(answer) is not int or not 1 <= answer <= 4:
            raise ValueError("정답은 1~4 사이의 정수여야 합니다.")

        if not isinstance(hint, str) or not hint.strip():
            raise ValueError("힌트는 빈 문자열일 수 없습니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer
        self.hint = hint.strip()

    def display(self):
        print(self.question)
        print()

        for idx, choice in enumerate(self.choices, start=1):
            print(f"{idx}. {choice}")

    def show_hint(self):
        print(f"💡 힌트: {self.hint}")

    def is_correct(self, user_answer):
        return self.answer == user_answer

    def to_dict(self):
        return {
            "question": self.question,
            "choices": self.choices,
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("퀴즈 데이터는 딕셔너리여야 합니다.")

        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data.get("hint", "등록된 힌트가 없습니다."),
        )