from fastapi import FastAPI, Request, Depends, Form, Response, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base, DarsModel, UserModel, IzohModel, SavolModel

Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

ADMIN_LOGIN = "Admin"
ADMIN_PASSWORD = "the_begi_37"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home(request: Request, db: Session = Depends(get_db), admin_session: str = Cookie(None), user_session: str = Cookie(None)):
    darslar = db.query(DarsModel).all()
    is_admin = (admin_session == "authenticated")
    is_logged_in = (admin_session == "authenticated" or user_session is not None)
    return templates.TemplateResponse(request, "index.html", {
        "darslar": darslar, 
        "is_admin": is_admin, 
        "is_logged_in": is_logged_in,
        "username": user_session
    })

@app.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html", {"request": request})

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if username == ADMIN_LOGIN and password == ADMIN_PASSWORD:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="admin_session", value="authenticated")
        return response
    
    user = db.query(UserModel).filter(UserModel.username == username, UserModel.password == password).first()
    if user:
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="user_session", value=user.username)
        return response
        
    return RedirectResponse(url="/login?error=1", status_code=303)

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie(key="admin_session")
    response.delete_cookie(key="user_session")
    return response

@app.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html", {"request": request})

@app.post("/register")
def register(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == username).first()
    if existing_user:
        return RedirectResponse(url="/register?error=exists", status_code=303)
    
    new_user = UserModel(username=username, password=password)
    db.add(new_user)
    db.commit()
    return RedirectResponse(url="/login", status_code=303)

# Shaxsiy profil sahifasi
@app.get("/profile")
def profile_page(request: Request, db: Session = Depends(get_db), user_session: str = Cookie(None), admin_session: str = Cookie(None)):
    if not user_session and admin_session != "authenticated":
        return RedirectResponse(url="/login", status_code=303)
    
    current_user = admin_session == "authenticated" and "Admin" or user_session
    # Foydalanuvchining o'z savollari
    savollar = db.query(SavolModel).filter(SavolModel.username == current_user).all()
    
    return templates.TemplateResponse(request, "profile.html", {
        "username": current_user,
        "savollar": savollar,
        "is_admin": admin_session == "authenticated"
    })

# Adminga savol yuborish
@app.post("/savol-yuborish")
def send_question(matn: str = Form(...), db: Session = Depends(get_db), user_session: str = Cookie(None), admin_session: str = Cookie(None)):
    current_user = admin_session == "authenticated" and "Admin" or user_session
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    new_savol = SavolModel(username=current_user, matn=matn)
    db.add(new_savol)
    db.commit()
    return RedirectResponse(url="/profile", status_code=303)

@app.get("/dars/{dars_id}")
def dars_detail(request: Request, dars_id: int, db: Session = Depends(get_db), admin_session: str = Cookie(None), user_session: str = Cookie(None)):
    dars = db.query(DarsModel).filter(DarsModel.id == dars_id).first()
    izohlar = db.query(IzohModel).filter(IzohModel.dars_id == dars_id).all()
    is_admin = (admin_session == "authenticated")
    is_logged_in = (admin_session == "authenticated" or user_session is not None)
    
    return templates.TemplateResponse(request, "dars_detail.html", {
        "dars": dars, 
        "izohlar": izohlar,
        "is_admin": is_admin,
        "is_logged_in": is_logged_in,
        "current_user": admin_session == "authenticated" and "Admin" or user_session
    })

# Darsga izoh qo'shish
@app.post("/dars/{dars_id}/izoh")
def add_comment(dars_id: int, matn: str = Form(...), db: Session = Depends(get_db), user_session: str = Cookie(None), admin_session: str = Cookie(None)):
    current_user = admin_session == "authenticated" and "Admin" or user_session
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    new_izoh = IzohModel(dars_id=dars_id, username=current_user, matn=matn)
    db.add(new_izoh)
    db.commit()
    return RedirectResponse(url=f"/dars/{dars_id}", status_code=303)

@app.get("/dars/{dars_id}/tahrirlash")
def dars_edit_form(request: Request, dars_id: int, db: Session = Depends(get_db), admin_session: str = Cookie(None)):
    if admin_session != "authenticated":
        return RedirectResponse(url="/login", status_code=303)
    dars = db.query(DarsModel).filter(DarsModel.id == dars_id).first()
    return templates.TemplateResponse(request, "dars_tahrirlash.html", {"dars": dars, "is_admin": True})

@app.post("/dars/{dars_id}/tahrirlash")
def dars_edit(
    dars_id: int,
    nomi: str = Form(...),
    daraja: str = Form(...),
    tavsif: str = Form(...),
    video_url: str = Form(None),
    kodlar: str = Form(None),
    db: Session = Depends(get_db),
    admin_session: str = Cookie(None)
):
    if admin_session != "authenticated":
        return RedirectResponse(url="/login", status_code=303)
    
    dars = db.query(DarsModel).filter(DarsModel.id == dars_id).first()
    if dars:
        dars.nomi = nomi
        dars.daraja = daraja
        dars.tavsif = tavsif
        dars.video_url = video_url
        dars.kodlar = kodlar
        db.commit()
    return RedirectResponse(url=f"/dars/{dars_id}", status_code=303)

@app.get("/dars/{dars_id}/ochirish")
def dars_delete(dars_id: int, db: Session = Depends(get_db), admin_session: str = Cookie(None)):
    if admin_session != "authenticated":
        return RedirectResponse(url="/login", status_code=303)
        
    dars = db.query(DarsModel).filter(DarsModel.id == dars_id).first()
    if dars:
        db.delete(dars)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
    
    # Yangi dars qo'shish sahifasi (GET)
@app.get("/dars-qoshish")
def dars_qoshish_form(request: Request, admin_session: str = Cookie(None)):
    if admin_session != "authenticated":
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse(request, "dars_qoshish.html", {"request": request, "is_admin": True})

# Yangi darsni saqlash (POST)
@app.post("/dars-qoshish")
def dars_qoshish(
    nomi: str = Form(...),
    daraja: str = Form(...),
    tavsif: str = Form(...),
    video_url: str = Form(None),
    kodlar: str = Form(None),
    db: Session = Depends(get_db),
    admin_session: str = Cookie(None)
):
    if admin_session != "authenticated":
        return RedirectResponse(url="/login", status_code=303)
    
    yangi_dars = DarsModel(
        nomi=nomi,
        daraja=daraja,
        tavsif=tavsif,
        video_url=video_url,
        kodlar=kodlar
    )
    db.add(yangi_dars)
    db.commit()
    return RedirectResponse(url="/", status_code=303)
