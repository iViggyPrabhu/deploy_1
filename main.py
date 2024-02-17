from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

class Name(BaseModel):
    first_name: str
    last_name: str

@app.get("/", response_class=HTMLResponse)
async def main():
    content = """
    <html>
        <head>
            <title>Greeting Page</title>
            <!-- Include Bootstrap CSS -->
            <link href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <!-- Bootstrap header with blue background -->
            <header class="bg-primary text-white text-center p-3">
                <h1>Learning DevOps</h1>
                <p id="currentTime">Current time: </p>
            </header>
            
            <div class="container mt-4">
                <h2>Enter your name</h2>
                <form action="/greet" method="post" id="nameForm">
                    <input type="text" name="first_name" placeholder="First Name" required class="form-control mb-2">
                    <input type="text" name="last_name" placeholder="Last Name" required class="form-control mb-2">
                    <button type="submit" class="btn btn-primary">Greet Me!</button>
                </form>
                <div id="greetingMessage" class="alert alert-success mt-3" style="display:none;"></div>
            </div>
            
            <script>
    // Function to update time
    function updateTime() {
        const currentTimeElement = document.getElementById('currentTime');
        const timeNow = new Date().toLocaleTimeString();
        currentTimeElement.innerText = 'Current time: ' + timeNow;
    }
    updateTime();
    setInterval(updateTime, 1000);  // Update the time every second

    // Handling the form submission
    const form = document.getElementById('nameForm');
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(form);
        fetch('/greet', {
            method: 'POST',
            body: JSON.stringify({
                first_name: formData.get('first_name'),
                last_name: formData.get('last_name')
            }),
            headers: {
                'Content-Type': 'application/json'
            },
        }).then(response => response.json()).then(data => {
            const greetingMessageElement = document.getElementById('greetingMessage');
            greetingMessageElement.innerText = data.message;
            greetingMessageElement.style.display = 'block';  // Ensure the message is visible
            // Optionally, scroll to bottom to bring the message into view
            window.scrollTo(0, document.body.scrollHeight);
        }).catch(error => console.error('Error:', error));
    });
</script>
        </body>
    </html>
    """
    return content

@app.post("/greet")
async def greet_name(name: Name):
    # Respond with a greeting message that includes the provided names
    print(f"{name.first_name}")
    print(f"{name.last_name}")
    return {"message": f"Hello {name.first_name} {name.last_name}"}