from fastapi import FastAPI, Header, HTTPException

app = FastAPI()


@app.get("/headers")
async def show_headers(user_agent: str = Header(),
                       accept_language: str | None = Header(default=None)):
    if user_agent and accept_language:
        return {"User-Agent": user_agent,
                "Accept-Language": accept_language}
    else:
        raise HTTPException(status_code=400, detail="Ошибка! Какой-то из заголовков отсутствует")

