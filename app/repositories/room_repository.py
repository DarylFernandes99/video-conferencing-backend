from app.db.redis import redis_client

class RoomRepository:
    """
    Manages active room state in Redis.
    Keys: 
        room:{room_id}:members -> Set of user_ids
        user:{user_id}:room -> room_id (Quick lookup where a user is)
    """
    
    async def add_user_to_room(self, room_id: str, user_id: str):
        await redis_client.sadd(f"room:{room_id}:members", user_id)
        await redis_client.set(f"user:{user_id}:room", room_id)
        
    async def remove_user_from_room(self, room_id: str, user_id: str):
        await redis_client.srem(f"room:{room_id}:members", user_id)
        await redis_client.delete(f"user:{user_id}:room")
        
    async def get_room_members(self, room_id: str):
        members = await redis_client.smembers(f"room:{room_id}:members")
        return list(members)

    async def get_user_room(self, user_id: str):
        return await redis_client.get(f"user:{user_id}:room")

room_repository = RoomRepository()
