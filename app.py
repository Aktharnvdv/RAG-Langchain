from flask import Flask, request, jsonify
from base_agent import process_request_task

app = Flask(__name__)

# Endpoint for receiving user input and initiating language processing
@app.route('/chat', methods=['POST'])
def chat():
    try:
        # Parse JSON data from the request
        data = request.json
        user_input = data.get('input', '')
        print(f"Received user input: {user_input}")

    except Exception as e:
        # Return an error response if JSON parsing fails
        return jsonify({"error": f"Error parsing JSON: {str(e)}"})

    # Check if user wants to exit
    if user_input.lower() in ['exit', 'quit', 'q']:
        return jsonify({"response": "Exiting the program."})

    try:
        # Enqueue a Celery task for processing user input
        task = process_request_task.apply_async(args=[user_input])
        return {"task_id": task.id, "status": "Task enqueued. Please wait for some time."}

    except Exception as e:
        # Return an error response if task enqueuing fails
        return {"error": str(e)}

# Endpoint for retrieving the result of a language processing task
@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    try:
        # Get the status and result of the Celery task
        task = process_request_task.AsyncResult(task_id)
        if task.ready():
            return jsonify({'status': 'Task completed', 'result': task.result})
        else:
            return jsonify({'status': 'Task is still running. Please wait for some time.'})

    except Exception as e:
        # Return an error response if task result retrieval fails
        return jsonify({'status': 'Error', 'message': str(e)})

# Run the Flask application in debug mode if executed directly
if __name__ == '__main__':
    app.run(debug=True)
