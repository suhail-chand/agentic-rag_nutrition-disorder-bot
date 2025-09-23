from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser 

from config import llm
from agents.prompts import PRECISION


def check_precision(state: dict) -> dict:
    """
    Checks whether the response precisely addresses the user's query.

    Args:
        state (dict): The current state of the workflow, containing the query and response.

    Returns:
        dict: The updated state with the precision score.
    """
    print("-"*20, "check_precision", "-"*20)
    
    precision_prompt = ChatPromptTemplate.from_messages([
        ("system", PRECISION["system"]),
        ("user", PRECISION["query"])
    ])

    chain = precision_prompt | llm | StrOutputParser()

    precision_score = float(chain.invoke({
        "query": state['query'],
        "response": state['response']
    }))

    state['precision_score'] = precision_score
    state["precision_loop_count"] += 1

    print(" precision_score:", precision_score)
    print(" precision_loop_count:", state["precision_loop_count"])

    return state


def should_continue_precision(state: dict) -> str:
    """
    Decide if precision is sufficient or needs improvement.
    """
    print("-"*20, "should_continue_precision", "-"*20)

    if state['precision_score'] >= 4.0:
        print(" Precision score threshold met. Ending workflow.")
        return "pass"
    else:
        if state["precision_loop_count"] > state['loop_max_iter']:
            return "max_iterations_reached"
        else:
            print(f" Precision Score Threshold Not met. Refining Query.")
            return "refine_query"