
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import run_agent
from tools import reserve_book

app = FastAPI(title="AI Library Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


class ReservationRequest(BaseModel):
    book_id: int
    customer_name: str
    confirmed: bool


@app.get("/")
def home():
    return {"message": "AI Library Assistant API is running"}


@app.post("/chat")
def chat(request: ChatRequest):

    try:
        return run_agent(request.message)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/confirm-reservation")
def confirm_reservation(request: ReservationRequest):

    if not request.confirmed:
        return {
            "status": "cancelled",
            "message": "Reservation cancelled."
        }

    result = reserve_book(
        book_id=request.book_id,
        customer_name=request.customer_name,
        confirmed=True
    )

    return result
