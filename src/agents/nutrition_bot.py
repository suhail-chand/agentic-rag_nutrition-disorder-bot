from datetime import datetime
from mem0 import MemoryClient
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.agents import (AgentExecutor, 
                              create_tool_calling_agent)

from agents.prompts import AGENT
from config import (MEM0_API_KEY, 
                    OPENAI_API_KEY, 
                    OPENAI_API_BASE)
from agents.tool import agentic_rag


class NutritionBot:
    def __init__(self):
        """
        Initialize the NutritionBot class, setting up memory, the LLM client, tools, and the agent executor.
        """

        # Initialize a memory client to store and retrieve customer interactions
        self.memory = MemoryClient(api_key=MEM0_API_KEY)

        # Initialize the OpenAI client using the provided credentials
        self.client = ChatOpenAI(
            model_name="gpt-4o-mini",
            openai_api_key=OPENAI_API_KEY,
            openai_api_base=OPENAI_API_BASE,
            temperature=0
        )

        # Define tools available to the chatbot, such as web search
        tools = [agentic_rag]

        # Build the prompt template for the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", AGENT["system"]),                        # System instructions
            ("human", "{input}"),                               # Placeholder for human input
            ("placeholder", "{agent_scratchpad}")               # Placeholder for intermediate reasoning steps
        ])

        # Create an agent capable of interacting with tools and executing tasks
        agent = create_tool_calling_agent(self.client, tools, prompt)

        # Wrap the agent in an executor to manage tool interactions and execution flow
        self.agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


    def store_customer_interaction(self, user_id: str, message: str, response: str, metadata: dict = None):
        """
        Store customer interaction in memory for future reference.

        Args:
            user_id (str): Unique identifier for the customer.
            message (str): Customer's query or message.
            response (str): Chatbot's response.
            metadata (dict, optional): Additional metadata for the interaction.
        """
        if metadata is None:
            metadata = {}

        # Add a timestamp to the metadata for tracking purposes
        metadata["timestamp"] = datetime.now().isoformat()

        # Format the conversation for storage
        conversation = [
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ]

        # Store the interaction in the memory client
        self.memory.add(
            conversation,
            user_id=user_id,
            output_format="v1.1",
            metadata=metadata
        )


    def get_relevant_history(self, user_id: str, query: str) -> list[dict]:
        """
        Retrieve past interactions relevant to the current query.

        Args:
            user_id (str): Unique identifier for the customer.
            query (str): The customer's current query.

        Returns:
            list[dict]: A list of relevant past interactions.
        """
        return self.memory.search(
            query=query,            # Search for interactions related to the query
            user_id=user_id,        # Restrict search to the specific user
            limit=5                 # Limit for retrieved interactions
        )


    def handle_customer_query(self, user_id: str, query: str) -> str:
        """
        Process a customer's query and provide a response, taking into account past interactions.

        Args:
            user_id (str): Unique identifier for the customer.
            query (str): Customer's query.

        Returns:
            str: Chatbot's response.
        """

        # Retrieve relevant past interactions for context
        relevant_history = self.get_relevant_history(user_id, query)

        # Build a context string from the relevant history
        context = "Previous relevant interactions:\n"
        for memory in relevant_history:
            context += f"Customer: {memory['memory']}\n"    # Customer's past messages
            context += f"Support: {memory['memory']}\n"     # Chatbot's past responses
            context += "---\n"

        print("CONTEXT: ", context)

        # Prepare a prompt combining past context and the current query
        prompt = AGENT["query"].format(context=context, query=query)

        # Generate a response using the agent
        response = self.agent_executor.invoke({"input": prompt})

        # Store the current interaction for future reference
        self.store_customer_interaction(
            user_id=user_id,
            message=query,
            response=response["output"],
            metadata={"type": "support_query"}
        )

        # Return the chatbot's response
        return response['output']
    