import streamlit as st

from agent.nutrition_bot import NutritionBot
from utils.guardrail import filter_input_with_llama_guard


def nutrition_disorder_streamlit():
    """
    A Streamlit-based UI for the Nutrition Disorder Specialist Agent.
    """
    st.title("Nutrition Disorder Specialist")
    st.write("Ask me anything about nutrition disorders, symptoms, causes, treatments, and more.")
    st.write("Type 'exit' to end the conversation.")

    # Initialize session state for chat history and user_id if they don't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
        
    # Login form: Only if user is not logged in
    if st.session_state.user_id is None:
        with st.form("login_form", clear_on_submit=True):
            user_id = st.text_input("Please enter your name to begin:")
            submit_button = st.form_submit_button("Login")
            if submit_button and user_id:
                st.session_state.user_id = user_id
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": f"Welcome, {user_id}! How can I help you with nutrition disorders today?"
                })

                # Set flag to trigger rerun
                st.session_state.login_submitted = True
        if st.session_state.get("login_submitted", False):
            st.session_state.pop("login_submitted")
            st.rerun()
    else:
        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
        # Chat input with custom placeholder text
        user_query = st.chat_input("Type your question here (or 'exit' to end)...")
        if user_query:
            if user_query.lower() == "exit":
                st.session_state.chat_history.append({"role": "user", "content": "exit"})
                with st.chat_message("user"):
                    st.write("exit")
                goodbye_msg = "Goodbye! Feel free to return if you have more questions about nutrition disorders."
                st.session_state.chat_history.append({"role": "assistant", "content": goodbye_msg})
                with st.chat_message("assistant"):
                    st.write(goodbye_msg)
                st.session_state.user_id = None
                st.rerun()
                return

            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)

            # Filter input using Llama Guard
            filtered_result = filter_input_with_llama_guard(user_query)
            filtered_result = filtered_result.replace("\n", " ")        # Normalize the result

            # Check if input is safe based on allowed statuses
            if filtered_result in ["safe", "unsafe S6", "unsafe S7"]:
                try:
                    if 'chatbot' not in st.session_state:
                        st.session_state.chatbot = NutritionBot()
                    response = st.session_state.chatbot.handle_customer_query(st.session_state.user_id, user_query)

                    st.write(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Sorry, I encountered an error while processing your query. Please try again. Error: {str(e)}"
                    st.write(error_msg)
                    st.session_state.chat_history.append({"role": "assistant", "content": error_msg})
            else:
                inappropriate_msg = "I apologize, but I cannot process that input as it may be inappropriate. Please try again."
                st.write(inappropriate_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": inappropriate_msg})


if __name__ == "__main__":
    nutrition_disorder_streamlit()
