# from openai import OpenAI
# from fastapi import FastAPI, Form, Request, WebSocket
# from typing import Annotated
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# openai = OpenAI(
#     api_key = os.getenv('MY_OPENAI_KEY')
# )
#
# app = FastAPI()
#
# templates = Jinja2Templates(directory="templates")
#
# chat_responses = []
#
# @app.get("/", response_class=HTMLResponse)
# async def chat_page(request: Request):
#     return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})
#
#
# chat_log = [{'role': 'system',
#              'content': 'you are a tutor of programming. you know every languages of programming.'
#                         ' If you are asked something besides of programming, you will give a standard response like: '
#                         '" I dont know anything about this but I can help you with learning programming."'
#              }]
#
#
# @app.websocket("/ws")
# async def chat(websocket: WebSocket):
#
#     await websocket.accept()
#
#     while True:
#         user_input = await websocket.receive_text()
#         chat_log.append({'role': 'user', 'content': user_input})
#         chat_responses.append(user_input)
#
#         try:
#             response = openai.chat.completions.create(
#                 model='gpt-4o-mini',
#                 messages=chat_log,
#                 temperature=0.6,
#                 stream=True
#             )
#
#             ai_response = ''
#
#             for chunk in response:
#                 if chunk.choices[0].delta.content is not None:
#                     ai_response += chunk.choices[0].delta.content
#                     await websocket.send_text(chunk.choices[0].delta.content)
#             chat_responses.append(ai_response)
#
#         except Exception as e:
#             await websocket.send_text(f'Error: {str(e)}')
#             break
#
#
# @app.post("/", response_class=HTMLResponse)
# async def chat(request: Request, user_input: Annotated[str, Form()]):
#
#     chat_log.append({'role': 'user', 'content': user_input})
#     chat_responses.append(user_input)
#
#     response = openai.chat.completions.create(
#         model='gpt-4',
#         messages=chat_log,
#         temperature=0.6
#     )
#
#     bot_response = response.choices[0].message.content
#     chat_log.append({'role': 'assistant', 'content': bot_response})
#     chat_responses.append(bot_response)
#
#     return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


from openai import OpenAI
from fastapi import FastAPI, Form, Request
from typing import Annotated
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

import os
from dotenv import load_dotenv

load_dotenv()

openai = OpenAI(
    api_key = os.getenv('MY_OPENAI_KEY')
)
app = FastAPI()
@app.get("/")
def read_root():
    return {"message": "Hello, Vercel!"}

templates = Jinja2Templates(directory="templates")

chat_responses = []


@app.get("/", response_class=HTMLResponse)
async def chat_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})


chat_log = [{'role': 'system',
             'content': 'You are a Python tutor AI, completely dedicated to teach users how to learn \
                        Python from scratch. Please provide clear instructions on Python concepts, \
                        best practices and syntax. Help create a path of learning for users to be able \
                        to create real life, production ready python applications.'
             }]


@app.post("/", response_class=HTMLResponse)
async def chat(request: Request, user_input: Annotated[str, Form()]):

    chat_log.append({'role': 'user', 'content': user_input})
    chat_responses.append(user_input)

    response = openai.chat.completions.create(
        model='gpt-4o-mini',
        messages=chat_log,
        temperature=0.6
    )

    bot_response = response.choices[0].message.content
    chat_log.append({'role': 'assistant', 'content': bot_response})
    chat_responses.append(bot_response)

    return templates.TemplateResponse("home.html", {"request": request, "chat_responses": chat_responses})

















