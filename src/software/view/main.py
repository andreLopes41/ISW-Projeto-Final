from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from controller.password_controller import PasswordController
from pathlib import Path

app = FastAPI()

templates = Jinja2Templates(directory="view/templates")

messages = []

def get_messages(request: Request):
    """Função para gerenciar mensagens flash"""
    global messages
    current_messages = messages.copy()
    messages.clear()
    return current_messages

@app.get("/")
async def index(request: Request, msgs: list = Depends(get_messages)):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "messages": msgs}
    )

@app.get("/registrar")
async def register_get(request: Request, msgs: list = Depends(get_messages)):
    return templates.TemplateResponse(
        "registrar.html", 
        {"request": request, "messages": msgs}
    )

@app.post("/registrar")
async def register_post(
    request: Request,
    domain: str = Form(...),
    password: str = Form(...)
):
    try:
        controller = PasswordController()
        is_first, key = controller.create_password(domain, password)
        
        if is_first:
            messages.append({
                "type": "info", 
                "text": f'Sua chave de acesso é: {key} Guarde-a com segurança! Você precisará dela para consultar suas senhas.'
            })
        
        messages.append({"type": "success", "text": "Senha registrada com sucesso!"})
        return RedirectResponse(url="/", status_code=303)
        
    except ValueError as e:
        messages.append({"type": "warning", "text": str(e)})
        return RedirectResponse(url="/registrar", status_code=303)
    except Exception as e:
        messages.append({"type": "danger", "text": f"Erro ao registrar senha: {str(e)}"})
        return RedirectResponse(url="/registrar", status_code=303)

@app.get("/consultar")
async def consult_get(request: Request, msgs: list = Depends(get_messages)):
    return templates.TemplateResponse(
        "consultar.html", 
        {"request": request, "messages": msgs}
    )

@app.post("/consultar")
async def consult_post(
    request: Request,
    domain: str = Form(...),
    access_key: str = Form(...)
):
    try:
        controller = PasswordController()
        password = controller.get_password(domain, access_key)
        
        if password == "Chave de acesso inválida":
            messages.append({"type": "danger", "text": password})
        elif password == "Senha não encontrada":
            messages.append({"type": "warning", "text": password})
        else:
            messages.append({"type": "success", "text": f"Senha para {domain}: {password}"})
            
    except Exception as e:
        messages.append({"type": "danger", "text": f"Erro ao consultar senha: {str(e)}"})
    
    return RedirectResponse(url="/consultar", status_code=303)