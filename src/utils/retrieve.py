from langchain_community.vectorstores import Chroma

from config import (embedding_model, 
                    STORE_DIRECTORY, 
                    STORE_COLLECTION)


# Initialize the Chroma vector store for retrieving documents
vector_store = Chroma(
    collection_name=STORE_COLLECTION,
    persist_directory=STORE_DIRECTORY,
    embedding_function=embedding_model
)

# Create a retriever from the vector store
retriever = vector_store.as_retriever(
    search_type='similarity',
    search_kwargs={'k': 5}
)


def retrieve_context(state):
    """
    Retrieves context from the vector store using the expanded or original query.

    Args:
        state (dict): The current state of the workflow, containing the query and expanded query.

    Returns:
        dict: The updated state with the retrieved context.
    """
    print("-"*20, "retrieve_context", "-"*20)
    
    query = state['expanded_query']
    
    # print(" Query used for retrieval:", query)

    # Retrieve documents from the vector store
    docs = retriever.invoke(query)
    
    # print(" Retrieved documents:", docs)

    # Extract both page_content and metadata from each document
    context= [
        {
            "content": doc.page_content,        # The actual content of the document
            "metadata": doc.metadata            # The metadata (e.g., source, page number, etc.)
        }
        for doc in docs
    ]
    state['context'] = context
    
    # print("Extracted context with metadata:", context)

    return state
