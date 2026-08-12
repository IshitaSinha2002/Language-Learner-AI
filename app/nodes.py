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

def evaluate_answers(state: LearningState):
    quiz = state["quiz"]
    answers = state["answers"]

    correct = 0
    weaknesses = []

    for question, answer in zip(quiz, answers):
        if answer.strip().lower() == question["correct_answer"].strip().lower():
            correct +=1
        else:
            weaknesses.append(question["question"])

    total_questions = len(quiz)

    if total_questions == 0:
        score = 0.0
    else:
        score = (correct/total_questions) * 100

    return {
        "score": score,
        "weaknesses": weaknesses
    }

def update_progress(state: LearningState):
    score = state["score"]
    current_topic = state["current_topic"]
    weaknesses = state["weaknesses"]

    history = state["learning_history"].copy()
    mastered_topics = state["mastered_topics"].copy()

    session_record = {
        "topic": current_topic,
        "score": score,
        "weaknesses": weaknesses
    }

    history.append(session_record)

    if score >= 70 and current_topic not in mastered_topics:
        mastered_topics.append(current_topic)

    return {
        "learning_history": history,
        "mastered_topics": mastered_topics,
        "weaknesses": weaknesses
    }

def choose_next_topic(state: LearningState):
    score = state["score"]
    current_topic = state["current_topic"]
    mastered_topics = state["mastered_topics"]

    if score < 70:
        return {
            "next_topic": current_topic
        }

    topic_sequence = [
        "Basic Vocabulary",
        "Greetings",
        "Present Tense",
        "Past Tense",
        "Future Tense",
        "Conversation"
    ]

    if current_topic in topic_sequence:
        current_index = topic_sequence.index(current_topic)

        for topic in topic_sequence[current_index + 1:]:
            if topic not in mastered_topics:
                return {
                    "next_topic": topic
                }

    return {
        "next_topic": "Conversation"
    }