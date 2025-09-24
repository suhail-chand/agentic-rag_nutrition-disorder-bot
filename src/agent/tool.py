from langchain_core.tools import tool

from agent.workflow import WORKFLOW_APP


@tool
def agentic_rag(query: str):
    """
    Runs the RAG-based agent with conversation history for context-aware responses.

    Args:
        query (str): The current user query.

    Returns:
        dict[str, Any]: The updated state with the generated response and conversation history.
    """
    # Initialize state with necessary parameters
    inputs = {
        "query": query,                 # Current user query
        "expanded_query": "",           # Expanded version will be generated in the workflow
        "context": [],                  # Retrieved documents (initially empty)
        "response": "",                 # AI-generated response (to be filled by workflow)
        "precision_score": 0.0,         # Initial precision score
        "groundedness_score": 0.0,      # Initial groundedness score
        "groundedness_loop_count": 0,   # Start groundedness loop counter at 0
        "precision_loop_count": 0,      # Start precision loop counter at 0
        "feedback": "",                 # Initial feedback is empty
        "query_feedback": "",           # Initial query feedback is empty
        "loop_max_iter": 3              # Maximum number of iterations for loops
    }

    output = WORKFLOW_APP.invoke(inputs)

    return output
