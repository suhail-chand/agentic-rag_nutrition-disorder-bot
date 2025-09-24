# Base image with Python version
FROM python:3.9

# Username to be created
RUN useradd -m -u 1000 user

# Specify the username for subsequent commands
USER user

# PATH environment variable based on username
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Use the same username for file ownership when copying requirements
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Use the same username for file ownership when copying the app files
COPY --chown=user . /app

# Start the Streamlit app on port 7860, the default port expected by Spaces
CMD ["streamlit", "run", "src/app.py", "--server.port=7860", "--server.address=0.0.0.0"]
