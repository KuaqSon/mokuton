from django.core.files.storage import FileSystemStorage
from ninja import File, Form, NinjaAPI
from ninja.files import UploadedFile

from main_app.api import GlobalAuth, auth_router, users_router

api = NinjaAPI(auth=GlobalAuth())

api.add_router("/auth/", auth_router)
api.add_router("/users/", users_router)


@api.get("/hello")
def hello(request):
    return "Hello world"


@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}


@api.post("/token", auth=None)  # < overriding global auth
def get_token(request, username: str = Form(...), password: str = Form(...)):
    if username == "admin" and password == "123":
        return {"token": "supersecret"}


@api.post("/upload", auth=None)
def upload(request, file: UploadedFile = File(...)):
    fs = FileSystemStorage()
    saved_file = fs.save(file.name, file)
    uploaded_file_url = fs.url(saved_file)
    return {"name": file.name, "url": uploaded_file_url}
