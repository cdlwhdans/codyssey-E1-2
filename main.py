from quiz_game import QuizGame


def main():
    try:
        game = QuizGame()
        game.run()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 프로그램을 종료합니다.")

    
if __name__ == "__main__":
    main()
