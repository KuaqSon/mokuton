from .base import *

DEBUG = True


# # =============
# # CORS
# # =============
WEB_APP = "http://localhost:3000"
CORS_ALLOWED_ORIGIN_REGEXES = [
    WEB_APP,
    r"^http://\w+\.localhost:3000$",
    "http://0.0.0.0:3008",
    r"http://\w+\.ngrok.io$",
    r"https://\w+\.ngrok.io$",
]
