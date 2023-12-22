from fastapi import FastAPI, Depends, HTTPException, APIRouter
from starlette.requests import Request

app = FastAPI()

# yield
async def get_async_session():
    print("Получение сессии")
    session = "session"
    yield session
    print("Уничтожение сессии")


@app.get("/items")
async def get_items(session=Depends(get_async_session)):      # depends от получения сессии
    print(session)                                            # сессию получаем, перед этим открываем,
    return [{"id": 1}]                                        # после использования закрываем


# parameters
def pagination_params(limit: int = 10, skip: int = 0):
    return {"limit": limit, "skip": skip}

# при запуске программы отрабатывается что переменная pagination_params = pagination_params(), то есть вставляется dict
@app.get("/subjects")
async def get_subjects(pagination_params: dict = Depends(pagination_params)):
    return pagination_params


# class
class Paginator:
    def __init__(self, limit: int = 10, skip: int = 0):
        self.limit = limit
        self.skip = skip


@app.get("/subjects_class")
async def get_subjects_class(pagination_params: Paginator = Depends()):
    return pagination_params


# dependencies = [Depends(...)]
# class call
# request

class AuthGuard:
    def __init__(self, name: str):                           # при создании класса
        self.name = name

    def __call__(self, request: Request):                     # при создании экземпляра класса - проверяем авторизацию
        # проверяем что в куках есть инфа о наличии прав пользователя
        if "super_cookie" not in request.cookies:
            raise HTTPException(status_code=403, detail="Запрещено")
        return True


auth_guard_payments = AuthGuard("payments")      # здесь создаем  экземпляр класса

# --- Variant 1 Depends  в router – для всех end-point  этого router ----
#
# router = APIRouter(
#     dependencies=[Depends(auth_guard_payments)]           # - сюда экземпляр класса
# )

# ------------------ Variant 2 -----------------
# @app.get("/payments")
# def get_payments(auth_guard_payments: AuthGuard = Depends(auth_guard_payments)):   # здесь вызываем экземпляр класса,
#                                                                                 # кот.проверяет авторизацию
#     return "my payments...."

# ------------------ Variant 3 -----------------
@app.get("/payments", dependencies=[Depends(auth_guard_payments)])           # здесь вызываем экземпляр класса,
                                                                             # кот.проверяет авторизацию
def get_payments():                                                          # здесь м.б. другие параметры функции,
    return "my payments...."


