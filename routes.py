

#Part 1

from flask import Flask, make_response, jsonify, request
import dataset
import pandas as pd
app = Flask(__name__)
db = dataset.connect('sqlite:///test.db')



table = db['tasks']


def fetch_db(task_id):  
    return table.find_one(task_id=task_id)

def fetch_db_due(Due_date):
    due_date=[]
    Due_date = pd.to_datetime(Due_date)
    for task in table:
        if((pd.to_datetime(task['Due_date'])) == Due_date) and (task['Status'] != "Finished"):
            due_date.append(task)
    return due_date

def fetch_db_over(): 
    
    due_date=[]
    Due_date = pd.to_datetime('now')
    for task in table:
        if((pd.to_datetime(task['Due_date'])) <  Due_date) and (task['Status'] != "Finished"):
            due_date.append(task)
    return due_date
  
def fetch_db_finished(): 
  
    task_f=[]
  
    for task in table:
        if( (task['Status']) == "Finished"):
            task_f.append(task)
    return task_f
def fetch_db_all():
    tasks = []
    for task in table:
        tasks.append(task)
    return tasks


@app.route('/api/db_populate', methods=['GET'])
def db_populate():
    table.insert({
        "task_id": "1",
        "name": "Learn Python.",
        "author": "George R. R. Martin",
        "Due_date": "22/06/2021",
        "Status":  "In-Progress"
    })

    table.insert({
        "task_id": "2",
        "name": "Learn R.",
        "author": "George",
        "Due_date": "24/06/2021",
        "Status":  "Finished"
    })
    table.insert({
        "task_id": "3",
        "name": "Learn API.",
        "author": "Martin",
        "Due_date": "28/06/2021",
        "Status":  "Not Started"
    })
    return make_response(jsonify(fetch_db_all()),
                         200)


@app.route('/api/tasks', methods=['GET', 'POST'])
def api_tasks():
    if request.method == "GET":
        return make_response(jsonify(fetch_db_all()), 200)
    elif request.method == 'POST':
        content = request.json
     
        task_id = content['task_id']

        table.insert(content)
        return make_response(jsonify(fetch_db(task_id)), 201)  # 201 = Created


@app.route('/api/tasks/<task_id>', methods=['GET', 'PUT', 'DELETE'])
def api_each_task(task_id):
    if request.method == "GET":
        task_obj = fetch_db(task_id)
        if task_obj:
            return make_response(jsonify(task_obj), 200)
        else:
            return make_response(jsonify(task_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['task_id'])

        task_obj = fetch_db(task_id)
        return make_response(jsonify(task_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=task_id)

        return make_response(jsonify({}), 204)

@app.route('/api/tasks/Due_date/<Due_date>', methods=['GET', 'PUT', 'DELETE'])
def api_due_task(Due_date):
    if request.method == "GET":
        Due_obj = fetch_db_due(Due_date)
        if Due_obj:
            return make_response(jsonify(Due_obj), 200)
        else:
            return make_response(jsonify(Due_obj), 404)
    elif request.method == "PUT":  # Updates the book
        content = request.json
        table.update(content, ['Due_date'])

        Due_obj = fetch_db_due(Due_date)
        return make_response(jsonify(Due_obj), 200)
    elif request.method == "DELETE":
        table.delete(id=Due_date)

        return make_response(jsonify({}), 204)
@app.route('/api/tasks/over', methods=['GET', 'PUT', 'DELETE'])
def api_overdue_task():
    if request.method == "GET":
        Due_obj = fetch_db_over()
        if Due_obj:
            return make_response(jsonify(Due_obj), 200)
        else:
            return make_response(jsonify(Due_obj), 404)
        
@app.route('/api/tasks/finished', methods=['GET', 'PUT', 'DELETE'])
def api_finished_task():
    if request.method == "GET":
        Due_obj = fetch_db_finished()
        if Due_obj:
            return make_response(jsonify(Due_obj), 200)
        else:
            return make_response(jsonify(Due_obj), 404)        
        


        return make_response(jsonify({}), 204)
if __name__ == '__main__':
    
    app.run(debug=True, use_reloader=False)