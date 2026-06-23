content = '''{
  "deploy": {
    "startCommand": "uvicorn src.webhook_server:app --host 0.0.0.0 --port $PORT",
    "buildCommand": "pip install -r requirements.txt"
  }
}
'''
with open('railway.json', 'w', encoding='ascii', newline='\n') as f:
    f.write(content)
print("Done, length:", len(content))