from openai import OpenAI
from fastapi import FastAPI, Form, Request
import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

load_dotenv()
secret_key = os.getenv('MY_OPENAI_KEY')

client = OpenAI(
    api_key=secret_key
)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Conversation log variables and responses
chat_log = [{'role': 'system', 'content': 'You are a Python tutor AI, completely dedicated to teaching users how to learn Python from scratch. \
                                         Please provide clear instructions on Python concepts, \
                                         best practices and syntax. Help create a path of learning for users to be able to create \
                                         real-life, production-ready Python applications. \
                                         All questions besides Python, give a generic answer saying you cannot help me, \
                                         and you can only help me with Python. But you can answer questions like: Who are you? or What are you doing? or questions like that.'}]

chat_responses = []

@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    """Displays the main page with conversation history."""
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: str = Form(...)):
    """Process the POST request and redirect the user after processing."""
    # Add the user's question to the chat_log and the answers
    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    # Get the AI answer
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=chat_log,
        temperature=0.6
    )
    bot_response = response.choices[0].message.content
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    # Redirect the user to the main page
    return RedirectResponse("/", status_code=303)
