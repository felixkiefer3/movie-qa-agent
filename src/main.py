from src.agent import ask_movie_agent


def main():
    print("Movie QA Agent initialized. Type 'exit' to quit.\n")

    while True:
        user_input = input("> ")

        if user_input.lower() in ["exit", "quit"]:
            break

        if not user_input.strip():
            continue

        try:
            response = ask_movie_agent(user_input)
            print(f"\n{response}\n")
        except Exception as e:  # noqa: BLE001
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
