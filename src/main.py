from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.app.routers.users import router


description = """
BotofarmApp API helps you create testing users. 🚀
"""

app = FastAPI(
    title="BotofarmApp",
    description=description,
    summary="It is Botofarm",
    version="0.0.1",
    contact={
        "name": "Egor",
        "url": "https://github.com/Egorrrad",
    },
)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )




@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router)







