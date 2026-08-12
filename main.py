from langgraph.types import Command

from app.graph import build_graph


def main():
    graph = build_graph()

    learner_name = input("Enter your name: ")
    target_language = input("What language do you want to learn? ")
    learner_level = input("What is your current level? ")

    initial_state = {
        "learner_name": learner_name,
        "target_language": target_language,
        "learner_level": learner_level,
        "current_topic": "",
        "lesson": "",
        "quiz": [],
        "answers": [],
        "score": 0.0,
        "weaknesses": [],
        "mastered_topics": [],
        "learning_history": [],
        "next_topic": ""
    }

    config = {
        "configurable": {
            "thread_id": learner_name
        }
    }

    result = graph.invoke(
        initial_state,
        config
    )

    print("\n" + "=" * 60)
    print("LESSON")
    print("=" * 60)
    print(result["lesson"])

    print("\n" + "=" * 60)
    print("QUIZ")
    print("=" * 60)

    quiz = result["quiz"]

    for index, question in enumerate(quiz, start=1):
        print(f"\n{index}. {question['question']}")

        for option_index, option in enumerate(
            question["options"],
            start=1
        ):
            print(f"   {option_index}. {option}")

    answers = []

    print("\nEnter your answers:")

    for index, question in enumerate(quiz, start=1):
        answer = input(f"Question {index}: ")
        answers.append(answer)

    result = graph.invoke(
        Command(resume=answers),
        config
    )

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)

    print(f"Score: {result['score']:.1f}%")

    if result["weaknesses"]:
        print("\nAreas to improve:")

        for weakness in result["weaknesses"]:
            print(f"- {weakness}")
    else:
        print("\nExcellent! No weaknesses identified.")

    print("\nMastered topics:")

    for topic in result["mastered_topics"]:
        print(f"- {topic}")

    print(f"\nNext topic: {result['next_topic']}")


if __name__ == "__main__":
    main()