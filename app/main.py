## pip3 install fastapi uvicorn

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime
import uvicorn
import sqlite3

app = FastAPI()

class TodoItem(BaseModel):
    todo: str

@app.get("/")
async def health_check():
    return {"status": "OK"}

@app.get("/routes")
async def get_endpoints():
    routes = []
    for route in app.routes:
        if hasattr(route, "path"):
            routes.append(route.path)
    return {"endpoints": routes}

@app.post("/todo_1")
async def create_todo(todo_item: TodoItem):
    return {"todo": todo_item.todo}

todos = []

@app.post("/todo_10")
async def create_todo_list(todo_item: TodoItem):
    todos.append(todo_item.todo)
    if len(todos) > 10:
        todos.pop(0)
    return {"todos": todos}

todos_100 = []
@app.post("/todo_100")
async def create_todo_list(todo_item: TodoItem):
    todos_100.append(todo_item.todo)
    if len(todos_100) > 100:
        todos_100.pop(0)
    return {"todos": todos_100}

@app.post("/todo_save_file")
async def save_todo(todo_item: TodoItem):
    with open("/data/todos.txt", "a") as file:
        file.write(todo_item.todo + "\n")
    with open("/data/todos.txt", "r") as file:
        todos = file.readlines()
    todos = [todo.strip() for todo in todos]
    return {"todos": todos}

# Create a connection to the SQLite database
conn = sqlite3.connect('/data/mydatabase.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store the todos
cursor.execute('''
    CREATE TABLE IF NOT EXISTS todos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        todo TEXT
    )
''')

@app.post("/todo_sqlite")
async def create_todo_sqlite(todo_item: TodoItem):
    # Insert the todo into the SQLite database
    cursor.execute('''
        INSERT INTO todos (todo) VALUES (?)
    ''', (todo_item.todo,))

    # Commit the changes to the database
    conn.commit()

    # Retrieve all todos from the database
    cursor.execute('''
        SELECT todo FROM todos
    ''')
    todos = [row[0] for row in cursor.fetchall()]

    return {"todos": todos}

# Close the cursor and the connection when the application stops
@app.on_event("shutdown")
def shutdown_event():
    cursor.close()
    conn.close()

if __name__ == "__main__":

    uvicorn.run("main:app", host="0.0.0.0", port=3000)
