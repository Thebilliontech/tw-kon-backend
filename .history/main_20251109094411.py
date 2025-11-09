from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from trading import generate_trade_signal, get_latest_price

app = FastAPI()

# Allow frontend CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TradeRequest(BaseModel):
    user_id: str
    symbol: str
    account_size: float = 1000  # Default account size in USD

class TradeResponse(BaseModel):
    symbol: str
    direction: str
    entry_price: float
    stop_loss: float
    take_profit: float
    quantity: int

@app.post("/api/trade", response_model=TradeResponse)
def trade_endpoint(request: TradeRequest):
    trade = generate_trade_signal(request.symbol.upper(), request.account_size)
    if not trade:
        return {
            "symbol": request.symbol,
            "direction": "hold",
            "entry_price": 0.0,
            "stop_loss": 0.0,
            "take_profit": 0.0,
            "quantity": 0
        }
    return trade
