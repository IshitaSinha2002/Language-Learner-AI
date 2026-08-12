import json
from pathlib import Path

from app.state import LearningState

LEARNERS_FILE = Path("data/learners.json")

def load_learner(state: LearningState):
    with open(LEARNERS_FILE, "r") as file:
        learners = json.load(file)

    learner_name = state["learner_name"]

    if learner_name in learners["learners"]:
        learner = learners["learners"][learner_name]

        return {
            "target_language": learner["target_language"],
            "learner_level": learner["learner_level"],
            "current_topic": learner["current_topic"],
            "weaknesses": learner["weaknesses"],
            "mastered_topics": learner["mastered_topics"],
            "learning_history": learner["learning_history"],
            "next_topic": learner["next_topic"],
        }

    return {
        "weaknesses": [],
        "mastered_topics": [],
        "learning_history": [],
        "current_topic": "",
        "next_topic": "",
    }

def analyze_progress(state: LearningState):
    history = state["learning_history"]
    weaknesses = state["weaknesses"]
    mastered_topics = state["mastered_topics"]

    if not history:
        return {
            "curent_topic": "Basic Vocabulary",
            "next_topic": "Basic Vocabulary"
        }

    last_session = history[-1]

    if last_session["score"] < 70:
        return {
            "current_topic": last_session["topic"],
            "next_topic": last_session["topic"]
        }

    return {
        "current_topic": state["next_topic"],
        "next_topic": state["next_topic"]
    }