from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .db import get_db
from .models import User
from .weather import fetch_today_weather

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def redirect(name: str, request: Request) -> RedirectResponse:
    return RedirectResponse(url=request.url_for(name), status_code=status.HTTP_303_SEE_OTHER)


def current_user_id(request: Request) -> int | None:
    return request.session.get("user_id")


@router.get("/")
def home(request: Request):
    if current_user_id(request):
        return redirect("dashboard", request)
    return redirect("login_page", request)


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "error": None})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    username = username.strip()
    if not username or not password:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username and password are required."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    if db.query(User).filter_by(username=username).first():
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Username already exists."},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = User(username=username)
    user.set_password(password)
    db.add(user)
    db.commit()
    return redirect("login_page", request)


@router.get("/login", name="login_page")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter_by(username=username.strip()).first()
    if not user or not user.verify_password(password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "Invalid username or password."},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    request.session["user_id"] = user.id
    request.session["username"] = user.username
    return redirect("dashboard", request)


@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return redirect("login_page", request)


@router.get("/dashboard", name="dashboard")
def dashboard(request: Request):
    if not current_user_id(request):
        return redirect("login_page", request)

    weather = None
    error = None
    config = request.app.state.config

    try:
        weather = fetch_today_weather(config)
    except Exception as exc:  # noqa: BLE001
        error = f"Could not load weather data from KMA API: {exc}"

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "username": request.session.get("username"),
            "weather": weather,
            "error": error,
        },
    )
