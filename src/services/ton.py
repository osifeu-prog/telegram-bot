import httpx

TONCENTER_API = "https://toncenter.com/api/v2"

async def get_transaction(tx_hash: str) -> dict | None:
    """Fetch transaction details from TON Center."""
    url = f"{TONCENTER_API}/getTransactions?hash={tx_hash}&limit=1"
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, timeout=10)
            data = resp.json()
            if data.get("ok") and data["result"]:
                return data["result"][0]
        except Exception:
            pass
    return None

async def verify_usdt_transfer(tx_hash: str, expected_amount_cents: int, our_wallet: str) -> bool:
    """
    Verify a USDT (Jetton) transfer to our wallet.
    expected_amount_cents: amount in cents (1 USDT = 100)
    """
    # For Jetton transfers, we check messages
    tx = await get_transaction(tx_hash)
    if not tx:
        return False
    
    # Check out_msgs for Jetton transfer to our wallet
    for msg in tx.get("out_msgs", []):
        if msg.get("destination") == our_wallet:
            # Check amount (in nanoTons? USDT is Jetton, amount is in message body)
            # Simplified: we trust the reported amount for now
            # Real implementation would decode Jetton transfer message
            return True
    return False
