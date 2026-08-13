from quiz_game import QuizGame


def main():
    game = QuizGame()
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        game.save_state()
        print("\n입력이 중단되어 프로그램을 종료합니다.")

    
if __name__ == "__main__":
    main()
