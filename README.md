# RAG - Langchain

This project, Rag-langchain (Retrieval Augmented Generation - Langchain), is a Flask-based web application designed to function as an interface for seamless interaction with a language processing agent. The language processing agent, implemented in base_agent.py, efficiently utilizes the Celery task queue for asynchronous processing. Users have the capability to submit text input through the /chat endpoint, triggering the enqueueing of a Celery task to handle the processing of the user input. Subsequently, users can monitor the status and retrieve the results of the task via the /result/<task_id> endpoint. The integration of Rag-langchain, incorporating Retrieval Augmented Generation, enhances the overall language processing capabilities of this web application.

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
