from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 

from config import llm
from agents.prompts import GROUNDEDNESS


def score_groundedness(state: dict) -> dict:
    """
    Checks whether the response is grounded in the retrieved context.

    Args:
        state (dict): The current state of the workflow, containing the response and context.

    Returns:
        dict: The updated state with the groundedness score.
    """
    print("-"*20, "check_groundedness", "-"*20)

    groundedness_prompt = ChatPromptTemplate.from_messages([
        ("system", GROUNDEDNESS["system"]),
        ("user", GROUNDEDNESS["query"])
    ])

    chain = groundedness_prompt | llm | StrOutputParser()

    groundedness_score = float(chain.invoke({
        "context": "\n".join([doc["content"] for doc in state['context']]),
        "response": state['response']
    }))

    state['groundedness_score'] = groundedness_score
    state["groundedness_loop_count"] += 1

    print(" groundedness_score:", groundedness_score)
    print(" groundedness_loop_count:", state["groundedness_loop_count"])

    return state


def should_continue_groundedness(state):
    """
    Decide if groundedness is sufficient or needs improvement.
    """
    print("-"*20, "should_continue_groundedness", "-"*20)

    if state['groundedness_score'] >= 4.0:
        print(" Moving to precision")
        return "check_precision"
    else:
        if state["groundedness_loop_count"] > state['loop_max_iter']:
            return "max_iterations_reached"
        else:
            print(f" Groundedness Score Threshold Not met. Refining Response.")
            return "refine_response"
        