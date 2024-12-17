import os
import uvicorn
# from app import app 
from fastapi import FastAPI, Request, Response 
app = FastAPI(title='Whatsapp Bot Application') 

@app.get('/') 
async def home(request: Request): 
    return Response('<h1>Hello World</h1>', status_code=200) 

@app.post('/') 
async def create_something(request: Request): 
    payload = await request.json() 
    username = payload.get('username', 'none') 
    email = payload.get('email', 'none') 
    data = {'usernmae': username, 'email': email} 
    return data

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)