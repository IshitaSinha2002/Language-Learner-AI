from typing import TypedDict

class LearningState(TypedDict):
    learner_name: str
    target_language: str
    learner_level: str

    current_topic: str
    lesson: str
    quiz: list
    answers: list

    score: float
    weaknesses: list[str]
    mastered_topics: list[str]

    learning_history: list[dict]
    next_topic: str