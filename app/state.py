from typing import TypedDict


class QuizQuestion(TypedDict):
    question: str
    options: list[str]
    correct_answer: str


class LearningState(TypedDict):
    learner_name: str
    target_language: str
    learner_level: str

    current_topic: str
    lesson: str
    quiz: list[QuizQuestion]
    answers: list[str]

    score: float
    weaknesses: list[str]
    mastered_topics: list[str]

    learning_history: list[dict]
    next_topic: str