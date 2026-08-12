import json
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from app.prompts import LESSON_PROMPT
from app.state import LearningState


load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.3
)

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

    if not history:
        return {
            "current_topic": "Basic Vocabulary",
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


def generate_lesson(state: LearningState):
    prompt = ChatPromptTemplate.from_template(LESSON_PROMPT)

    chain = prompt | llm

    response = chain.invoke({
        "target_language": state["target_language"],
        "learner_level": state["learner_level"],
        "current_topic": state["current_topic"],
        "weaknesses": ", ".join(state["weaknesses"])
        if state["weaknesses"]
        else "None"
    })

    return {
        "lesson": response.content
    }