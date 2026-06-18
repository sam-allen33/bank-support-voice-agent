"""
mock_bank.py
------------
A tiny fake "core banking" API. This is the thing your ElevenLabs agent will
call when a caller asks "what's my balance?" or "what are my recent transactions?".

In a real bank this would be their actual systems. For learning, we just return
fixed pretend data so you can see the agent reach out, call this, and use the answer.

HOW TO RUN (in a terminal, from inside this folder):
    uvicorn mock_bank:app --reload --port 8000

Then open http://127.0.0.1:8000  in your browser. You should see a status message.
Test the endpoints in your browser too:
    http://127.0.0.1:8000/get_balance
    http://127.0.0.1:8000/list_transactions

You do NOT need to understand every line. You need to be able to run it and
explain what it does: "it's a fake bank API the agent calls through a tool."
"""

from fastapi import FastAPI, Request

app = FastAPI(title="Mock Bank API")

# --- Pretend account data (this is the "database") ---------------------------
DEMO_ACCOUNT = {
    "account_id": "demo-001",
    "name": "Alex Morgan",
    "currency": "USD",
    "balance": 1240.55,
    "available": 1190.55,  # balance minus a pending hold
}

RECENT_TRANSACTIONS = [
    {"date": "2026-06-15", "description": "Whole Foods Market", "amount": -86.20},
    {"date": "2026-06-14", "description": "Payroll deposit - Acme Inc", "amount": 2400.00},
    {"date": "2026-06-13", "description": "Spotify subscription", "amount": -11.99},
    {"date": "2026-06-12", "description": "Shell gas station", "amount": -52.30},
    {"date": "2026-06-11", "description": "Unknown charge - SP * GADGETS", "amount": -129.99},
]


async def _account_id(request: Request) -> str:
    """
    Figure out which account is being asked about.
    We accept it from a URL query (?account_id=demo-001) OR from a JSON body,
    and if neither is given we just fall back to the demo account.
    This makes the tool easy to configure no matter how you set it up.
    """
    aid = request.query_params.get("account_id")
    if aid:
        return aid
    try:
        body = await request.json()
        if isinstance(body, dict) and body.get("account_id"):
            return body["account_id"]
    except Exception:
        pass
    return DEMO_ACCOUNT["account_id"]


@app.get("/")
def health():
    """A simple 'I am alive' message so you can confirm the server is running."""
    return {"status": "ok", "service": "mock-bank", "try": ["/get_balance", "/list_transactions"]}


# The agent's "get_account_balance" tool will point at this URL.
@app.api_route("/get_balance", methods=["GET", "POST"])
async def get_balance(request: Request):
    aid = await _account_id(request)
    return {
        "account_id": aid,
        "currency": DEMO_ACCOUNT["currency"],
        "balance": DEMO_ACCOUNT["balance"],
        "available": DEMO_ACCOUNT["available"],
    }


# The agent's "list_recent_transactions" tool will point at this URL.
@app.api_route("/list_transactions", methods=["GET", "POST"])
async def list_transactions(request: Request):
    aid = await _account_id(request)
    return {"account_id": aid, "transactions": RECENT_TRANSACTIONS}
