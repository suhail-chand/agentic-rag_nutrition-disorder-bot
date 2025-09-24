from typing import Any, Dict, List, TypedDict
from langgraph.graph import StateGraph, END, START

from agent.generate import *
from utils.retrieve import retrieve_context
from evaluation.precision import (check_precision, 
                                  should_continue_precision)
from evaluation.groundedness import (score_groundedness, 
                                     should_continue_groundedness)


class AgentState(TypedDict):
    """
    Defines the AgentState class using TypedDict. 
    It represents the state of the AI agent at different stages of the workflow.
    """
    query: str                          # The current user query
    expanded_query: str                 # The expanded version of the user query
    context: List[Dict[str, Any]]       # Retrieved documents (content and metadata)
    response: str                       # The generated response to the user query
    precision_score: float              # The precision score of the response
    groundedness_score: float           # The groundedness score of the response
    groundedness_loop_count: int        # Counter for groundedness refinement loops
    precision_loop_count: int           # Counter for precision refinement loops
    feedback: str                       # Feedback from the user
    query_feedback: str                 # Feedback specifically related to the query
    groundedness_check: bool            # Indicator for groundedness check
    loop_max_iter: int                  # Maximum iterations for loops


def create_workflow() -> StateGraph:
    """
    Creates the updated workflow for the AI nutrition agent.
    """
    workflow = StateGraph(AgentState)

    # Add processing nodes
    workflow.add_node("expand_query", expand_query)                         # Step 1: Expand user query.
    workflow.add_node("retrieve_context", retrieve_context)                 # Step 2: Retrieve relevant documents.
    workflow.add_node("craft_response", craft_response)                     # Step 3: Generate a response based on retrieved data.
    workflow.add_node("score_groundedness", score_groundedness)             # Step 4: Evaluate response grounding.
    workflow.add_node("refine_response", refine_response)                   # Step 5: Improve response if it's weakly grounded.
    workflow.add_node("check_precision", check_precision)                   # Step 6: Evaluate response precision.
    workflow.add_node("refine_query", refine_query)                         # Step 7: Improve query if response lacks precision.
    workflow.add_node("max_iterations_reached", max_iterations_reached)     # Step 8: Handle max iterations.

    # Main flow edges
    workflow.add_edge(START, "expand_query")
    workflow.add_edge("expand_query", "retrieve_context")
    workflow.add_edge("retrieve_context", "craft_response")
    workflow.add_edge("craft_response", "score_groundedness")

    # Conditional edges based on groundedness check
    workflow.add_conditional_edges(
        "score_groundedness",
        should_continue_groundedness,
        {
            "check_precision": "check_precision",                   # If grounded, check precision.
            "refine_response": "refine_response",                   # If not grounded, refine response.
            "max_iterations_reached": "max_iterations_reached"      # If max loops reached, exit.
        }
    )

    # Go back to crafting a new response adopting feedback.
    workflow.add_edge("refine_response", "craft_response")

    # Conditional edges based on precision check
    workflow.add_conditional_edges(
        "check_precision",
        should_continue_precision,
        {
            "pass": END,                                            # If precise, complete the workflow.
            "refine_query": "refine_query",                         # If imprecise, refine the query.
            "max_iterations_reached": "max_iterations_reached"      # If max loops reached, exit.
        }
    )

    # Go through expansion again adopting feedback.
    workflow.add_edge("refine_query", "expand_query")

    workflow.add_edge("max_iterations_reached", END)

    return workflow


WORKFLOW_APP = create_workflow().compile()
