---
title: Nutri Care
emoji: 💪
colorFrom: red
colorTo: red
sdk: docker
pinned: false
---

# Agentic RAG Nutrition Disorder Specialist Bot

## Overview

Agentic RAG Nutrition Disorder Specialist Bot is an AI-powered chatbot designed to deliver accurate, evidence-based information and support on nutritional disorders. Leveraging an Agentic Retrieval-Augmented Generation (RAG) system, it answers user queries with high precision, grounded in a curated knowledge base of nutritional science documents.

This application empowers healthcare providers to rapidly access information on symptoms, diagnoses, treatment plans, and more, eliminating the need for time-consuming manual searches. The RAG-based chatbot operates through a custom, advanced workflow featuring these core components:

- **Query Expansion:** Refines user queries to improve retrieval accuracy while preserving the original intent, ensuring the most relevant information is surfaced from the knowledge base.
- **Context Retrieval:** Selects pertinent documents from a vector store using the expanded or original query, providing the necessary context for informed responses.
- **Response Generation:** Produces accurate, informative answers strictly based on the retrieved context, maintaining reliability and adherence to trusted nutritional sources.
- **Groundedness Evaluation:** Verifies the factual alignment of generated responses with the retrieved context, enhancing the credibility and trustworthiness of the information.
- **Precision Evaluation:** Assesses how precisely the response addresses the user's specific query, ensuring relevance and practical value.
- **Response Refinement:** Offers constructive feedback to address gaps, ambiguities, or missing details, refining responses that do not meet groundedness or precision standards.
- **Query Refinement:** Suggests improvements to the expanded query for even greater retrieval precision in subsequent iterations.

These operations ensure that the AI delivers the most accurate and relevant responses possible, strictly adhering to nutritional disorder guidelines and manuals. By iteratively evaluating and refining both queries and responses, the system upholds the high standards required in healthcare contexts.

The platform is built with Python, features a Streamlit-based web interface, and supports deployment on Hugging Face Spaces. It utilizes ChromaDB for vector storage and retrieval, and is architected for modularity, extensibility, and robust evaluation.

### Agentic Workflow

![Workflow Diagram](https://raw.githubusercontent.com/suhail-chand/agentic-rag_nutrition-specialist-bot/main/images/workflow.jpeg)

---

## Features
- **Conversational AI**: Expert answers to nutrition disorder questions via natural language.
- **Agentic RAG Workflow**: Advanced query expansion, retrieval, and grounded response generation.
- **Curated Knowledge Base**: Allows vetted nutritional science PDFs and research.
- **Evaluation Suite**: Automatically checks factual accuracy and relevance.
- **Iterative Self-Improvement**: Refines queries and responses for higher quality.
- **Chat History with Mem0**: Maintains context for coherent conversations.
- **Guardrails with LlamaGuard**: Ensures safe, guideline-compliant queries.
- **Streamlit Interface**: Modern, user-friendly web app.
- **Flexible Deployment**: Dockerized for local or Hugging Face Spaces deployment.

---

## Project Structure

```
├── Dockerfile
├── hf_deploy.py
├── main.py
├── requirements.txt
├── README.md
├── data/
│   └── docs/
│   └── store/
│       └── nutritional_db/
│       └── research_db/
├── images/
├── notebooks/
│   └── agent.ipynb
│   └── data_processing.ipynb
├── src/
│   ├── app.py
│   ├── config.py
│   ├── agent/
│   │   ├── generate.py
│   │   ├── nutrition_bot.py
│   │   ├── tool.py
│   │   └── workflow.py
│   ├── evaluation/
│   │   ├── groundedness.py
│   │   └── precision.py
│   └── utils/
│       ├── guardrail.py
│       ├── prompts.py
│       └── retrieve.py
```

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/suhail-chand/agentic-rag_nutrition-specialist-bot
cd agentic-rag_nutrition-specialist-bot
```

### 2. Install Python Dependencies

It is recommended to use Python 3.9+ and a virtual environment.

```bash
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in the root directory with the following variables:

```
MEM0_API_KEY = "your_mem0_api_key_here"
GROQ_API_KEY = "your_groq_api_key_here"
OPENAI_API_KEY = "your_openai_api_key_here"
OPENAI_API_BASE = "your_openai_api_base_here"

# Required for data processing with LlamaParse
LLAMA_KEY = "your_llama_parse_key"

# Required for Hugging Face deployment
HF_TOKEN = "your_hugging_face_token"
HF_REPO_ID = "your_hf_space_repo_id"
```

### 4. Data Preparation

- Place your knowledge base PDFs in `data/docs/`. (A sample document is included.)
- Run the `notebooks/data_processing.ipynb` notebook to process documents and create/update vector stores.
- Vector stores are managed in `data/store/` (A vector store for nutritional data is included using the given sample PDF.)

### 5. Running Locally

```bash
streamlit run src/app.py --server.port=7860
```
The app will be available at [http://localhost:7860](http://localhost:7860)

---

## Deploy to Hugging Face Spaces

1. Setup a Hugging Face account and create a new [Space](https://huggingface.co/spaces).
2. Generate a Hugging Face access token and set your credentials in `.env` as above.
3. Add the environment variables to your Space settings.
4. Run the deployment script:

```bash
python hf_deploy.py
```
This will upload the code, data, and Dockerfile to your Hugging Face Space.

---

## Usage

1. Open the web app in your browser.
2. Enter your nutrition disorder-related question.
3. The bot will retrieve relevant information and generate a grounded response.

---

## Deployed App - [Nutri Care](https://huggingface.co/spaces/suhail-chand/nutri-care)

**Screenshot**:

![Deployed App Screenshot](https://raw.githubusercontent.com/suhail-chand/agentic-rag_nutrition-specialist-bot/main/images/app-screenshot.png)
