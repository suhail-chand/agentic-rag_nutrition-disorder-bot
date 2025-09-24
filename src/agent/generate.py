from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import llm
from utils.prompts import (GENERATE, 
                           EXPANSION, 
                           REFINEMENT, 
                           RESPONSE_REFINEMENT)


def craft_response(state: dict) -> dict:
    """
    Generates a response using the retrieved context, focusing on nutrition disorders.

    Args:
        state (dict): The current state of the workflow, containing the query and retrieved context.

    Returns:
        Dict: The updated state with the generated response.
    """
    print("-"*20, "craft_response", "-"*20)

    response_prompt = ChatPromptTemplate.from_messages([
        ("system", GENERATE["system"]),
        ("user", GENERATE["query"])
    ])

    chain = response_prompt | llm

    response = chain.invoke({
        "query": state['query'],
        "context": "\n".join([doc["content"] for doc in state['context']]),
        "feedback": state['query_feedback']
    })

    state["response"] = response
    print(" Intermediate response:", response)

    return state


def expand_query(state):
    """
    Expands the user query to improve retrieval of nutrition disorder-related information.

    Args:
        state (dict): The current state of the workflow, containing the user query.

    Returns:
        dict: The updated state with the expanded query.
    """
    print("-"*20, "expand_query", "-"*20)
    
    expand_prompt = ChatPromptTemplate.from_messages([
        ("system", EXPANSION["system"]),
        ("user", EXPANSION["query"])
    ])

    chain = expand_prompt | llm | StrOutputParser()
    expanded_query = chain.invoke({"query": state['query'], "query_feedback": state["query_feedback"]})

    state["expanded_query"] = expanded_query
    print(" expanded_query", expanded_query)

    return state


def refine_query(state: dict) -> dict:
    """
    Suggests improvements for the expanded query.

    Args:
        state (dict): The current state of the workflow, containing the query and expanded query.

    Returns:
        dict: The updated state with query refinement suggestions.
    """
    print("-"*20, "refine_query", "-"*20)
    
    refine_query = ChatPromptTemplate.from_messages([
        ("system", REFINEMENT["system"]),
        ("user", REFINEMENT["query"])
    ])

    chain = refine_query | llm | StrOutputParser()

    # Store refinement suggestions without modifying the original expanded query
    query_feedback = f"Previous Expanded Query: {state['expanded_query']}\nSuggestions: {chain.invoke({'query': state['query'], 'expanded_query': state['expanded_query']})}"
    
    state["query_feedback"] = query_feedback
    print(" query_feedback:", query_feedback)

    return state


def refine_response(state: dict) -> dict:
    """
    Suggests improvements for the generated response.

    Args:
        state (dict): The current state of the workflow, containing the query and response.

    Returns:
        dict: The updated state with response refinement suggestions.
    """
    print("-"*20, "refine_response", "-"*20)

    refine_response_prompt = ChatPromptTemplate.from_messages([
        ("system", RESPONSE_REFINEMENT["system"]),
        ("user", RESPONSE_REFINEMENT["query"])
    ])

    chain = refine_response_prompt | llm | StrOutputParser()

    # Store response suggestions in a structured format
    feedback = f"Previous Response: {state['response']}\nSuggestions: {chain.invoke({'query': state['query'], 'response': state['response']})}"
    
    state['feedback'] = feedback
    print(" feedback: ", feedback)

    return state


def max_iterations_reached(state: dict) -> dict:
    """
    Handles the case when the maximum number of iterations is reached.
    """
    print("-"*20, "max_iterations_reached", "-"*20)

    response = "I'm unable to refine the response further. Please provide more context or clarify your question."
    state['response'] = response

    return state
