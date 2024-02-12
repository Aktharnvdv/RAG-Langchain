from flask import Flask, request, jsonify
from base_agent import process_request_task

app = Flask(__name__)
@app.route('/chat', methods=['POST'])
def chat():
    try:
        
        data = request.json
        user_input = data.get('input', '')
        print(f"Received user input: {user_input}")

    except Exception as e:
        return jsonify({"error": f"Error parsing JSON: {str(e)}"})

    if user_input.lower() in ['exit', 'quit', 'q']:
        return jsonify({"response": "Exiting the program."})    
    try:
        task = process_request_task.apply_async(
            args=[user_input]
        )
        return {"task_id": task.id, "status": "Task enqueued and wait for some time"}

    except Exception as e:
        return {"error": str(e)}

@app.route('/result/<task_id>', methods=['GET'])
def get_result(task_id):
    try:
        task = process_request_task.AsyncResult(task_id)
        if task.ready():
            return jsonify({'status': 'Task completed', 
                            'result': task.result})
        else:
            return jsonify({'status': 'Task is still running wait for some time'})
    except Exception as e:
        return jsonify({'status': 'Error', 'message': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
