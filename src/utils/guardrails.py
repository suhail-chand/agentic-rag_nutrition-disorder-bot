from groq import Groq

from config import GROQ_API_KEY


llama_guard_client = Groq(api_key=GROQ_API_KEY)


def filter_input_with_llama_guard(user_input, model="meta-llama/llama-guard-4-12b"):
    """
    Filters user input using Llama Guard to ensure it is safe.

    Parameters:
    - user_input: The input provided by the user.
    - model: The Llama Guard model to be used for filtering (default is "meta-llama/llama-guard-4-12b").

    Returns:
    - The filtered and safe input.
    """
    try:
        # Create a request to Llama Guard to filter the user input
        response = llama_guard_client.chat.completions.create(
            messages=[{"role": "user", "content": user_input}],
            model=model,
        )
        # Return the filtered input
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with Llama Guard: {e}")
        return None
    