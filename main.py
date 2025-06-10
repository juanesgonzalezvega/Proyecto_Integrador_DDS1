from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from routers.players import api, web

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.include_router(api.router, prefix="/api", tags=["API"])
app.include_router(web.router, prefix="", tags=["Web"])

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("players/home.html", {"request": request})

@app.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/planning")
async def planning():
    return {
        "requirements": [
            "Interfaz HTML",
            "Navegación coherente",
            "Estilo constante",
            "Formulario con imágenes",
            "Consultas por ID, nombre o característica",
            "Consulta total de elementos",
            "Modificación total y parcial",
            "Eliminación con historial",
            "Endpoints informativos"
        ]
    }

@app.get("/design")
async def design():
    return {
        "architecture": "Modular con routers, modelos, operaciones y plantillas",
        "frontend": "Bulma CSS y Jinja2 templates",
        "backend": "FastAPI con manejo de CSV",
        "storage": "Archivos CSV para datos"
    }

@app.get("/objective")
async def objective():
    return {
        "goal": "Crear una aplicación web para gestionar jugadores y partidos del Team USA con interfaz amigable y API REST."
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "message": "Error en la solicitud",
            "detail": exc.detail,
            "path": request.url.path
        },
    )