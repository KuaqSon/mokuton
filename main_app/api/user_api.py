from ninja import Router

router = Router()


@router.get("/")
def list_users(request):
    return [
        {"a": 1},
        {"a": 1},
        {"a": 1},
        {"a": 1},
        {"a": 1},
        {"a": 1},
        {"a": 1},
        {"a": 1},
    ]
