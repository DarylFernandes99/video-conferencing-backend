from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import socketio
from app.services.signaling_service import signaling_service

# Socket.IO Setup
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio)

app = FastAPI()

# Mount Socket.IO
app.mount("/socket.io", socket_app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Meet Clone Backend Running"}

@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Socket.IO Event Handlers ---

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    # In a real app, strict auth would happen here.
    # For MVP, we allow connection and handle logic in 'join_room'

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")
    room_id = await signaling_service.leave_room(sid)
    if room_id:
        await sio.emit('user-disconnected', sid, room=room_id)

@sio.event
async def join_room(sid, data):
    # data expects {'roomId': '...'}
    room_id = data.get('roomId')
    if not room_id:
        return
    
    print(f"User {sid} joining room {room_id}")
    await sio.enter_room(sid, room_id)
    
    # Get peers already in room
    peers = await signaling_service.join_room(room_id, sid)
    
    # Notify others in room
    await sio.emit('user-connected', sid, room=room_id, skip_sid=sid)
    
    # Return existing peers to the joining user (needed for Mesh initiation)
    # Socket.IO callbacks are supported, but direct emit is often easier to debug
    # We can return data to the acknowledgement callback
    return peers

@sio.event
async def offer(sid, data):
    # data: {'offer': ..., 'to': target_sid}
    target_sid = data.get('to')
    offer_sdp = data.get('offer')
    if target_sid:
        await sio.emit('offer', {'offer': offer_sdp, 'from': sid}, to=target_sid)

@sio.event
async def answer(sid, data):
    target_sid = data.get('to')
    answer_sdp = data.get('answer')
    if target_sid:
        await sio.emit('answer', {'answer': answer_sdp, 'from': sid}, to=target_sid)

@sio.event
async def ice_candidate(sid, data):
    target_sid = data.get('to')
    candidate = data.get('candidate')
    if target_sid:
        await sio.emit('ice-candidate', {'candidate': candidate, 'from': sid}, to=target_sid)
