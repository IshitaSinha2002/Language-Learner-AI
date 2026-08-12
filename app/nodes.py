import json
from pathlib import Path
from pydantic import BaseModel, Field

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

class QuizQuestionOutput(BaseModel):
    question: str = Field(description="The quiz question")
    options: list[str] = Field(description="Exactly four answer options")
    correct_answer: str = Field(description="The correct answer")


class QuizOutput(BaseModel):
    questions: list[QuizQuestionOutput] = Field(
        description="Exactly five quiz questions"
    )

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

def generate_quiz(state: LearningState):
    prompt = ChatPromptTemplate.from_template(QUIZ_PROMPT)

    structured_llm = llm.with_structured_output(QuizOutput)

    chain = prompt | structured_llm

    response = chain.invoke({
        "target_language": state["target_language"],
        "learner_level": state["learner_level"],
        "current_topic": state["current_topic"],
        "lesson": state["lesson"]
    })

    quiz = [
        question.model_dump()
        for question in response.questions
    ]

    return {
        "quiz": quiz
    }