from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt

from app.state import LearningState
from app.nodes import (
    load_learner,
    analyze_progress,
    generate_lesson,
    generate_quiz,
    evaluate_answers,
    update_progress,
    choose_next_topic,
    save_learner,
)

def build_graph():
    workflow = StateGraph(LearningState)

    workflow.add_node("load_learner", load_learner)
    workflow.add_node("analyze_progress", analyze_progress)
    workflow.add_node("generate_lesson", generate_lesson)
    workflow.add_node("generate_quiz", generate_quiz)
    workflow.add_node("evaluate_answers", evaluate_answers)
    workflow.add_node("update_progress", update_progress)
    workflow.add_node("choose_next_topic", choose_next_topic)
    workflow.add_node("save_learner", save_learner)

    workflow.add_edge(START, "load_learner")
    workflow.add_edge("load_learner", "analyze_progress")
    workflow.add_edge("analyze_progress", "generate_lesson")
    workflow.add_edge("generate_lesson", "generate_quiz")
    workflow.add_edge("generate_quiz", "evaluate_answers")
    workflow.add_edge("evaluate_answers", "choose_next_topic")
    workflow.add_edge("choose_next_topic", "update_progress")
    workflow.add_edge("update_progress", "save_learner")
    workflow.add_edge("save_learner", END)

    memory = MemorySaver()

    return workflow.compile(checkpointer=memory)