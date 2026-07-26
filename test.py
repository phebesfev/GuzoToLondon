import httpx

with httpx.Client(transport=httpx.HTTPTransport(local_address="0.0.0.0")) as client:
    r = client.get("https://api.telegram.org", timeout=15)
    print(r.status_code)