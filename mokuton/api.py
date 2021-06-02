from ninja import Form, NinjaAPI

from main_app.api import users_router

from .bearer_auth import GlobalAuth

api = NinjaAPI(auth=GlobalAuth())

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
