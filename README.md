# RAG - Langchain

#  Project Overview:
    
    The project is named Rag-langchain (Retrieval Augmented Generation - Langchain).
    It is a Flask-based web application serving as an interface for interacting with a language processing agent.
    Language Processing Agent:
    
    The language processing agent is implemented in base_agent.py.
    It leverages the Celery task queue for efficient asynchronous processing.
    
#  User Interaction:
    
    Users can submit text input to the /chat endpoint.
    This action triggers the enqueueing of a Celery task to process the user input.

#  Task Monitoring:
    
    Users can check the status and results of the task through the /result/<task_id> endpoint.
#  Integration Benefits:
    Rag-langchain integrates Retrieval Augmented Generation, enhancing the language processing capabilities of the web application.

By combining the capabilities of Rag-langchain with the existing features, the project provides a robust and effective solution for interacting with a language processing agent in a web environment.

# Usage
Prerequisites
Python 3.x
Flask
Celery
Redis

Installation
Install dependencies:

```bash
pip install flask celery
```
Set up Redis as the Celery broker and backend. Update the Celery configuration in app.py accordingly.

Obtain an API key for the AI21 language model and set it as an environment variable:

```bash
export AI21_API_KEY="your_api_key"
```
Running the Application
Run the Celery worker:

```bash
celery -A app.celery worker --loglevel=info
```
Run the Flask application:

```bash
python app.py
```
Access the application at http://localhost:5000 and submit a text input to the /chat endpoint.

# Files
app.py
This file contains the Flask application that handles user requests. Users can submit text inputs to the /chat endpoint, which enqueues a Celery task to process the input asynchronously. The status and result of the task can be checked at the /result/<task_id> endpoint.

# base_agent.py
This file defines a Celery task (process_request_task) that invokes a language processing agent. The agent is created using the AI21 language model and a set of tools for information retrieval. The agent processes user inputs asynchronously and returns the response or an error.

# Configuration
The Celery configuration is set in app.py, including the broker and backend configurations.
The AI21 API key is set as an environment variable.

Notes
The application is currently configured to use a Redis server for Celery. Make sure to have a Redis server running and properly configured.
