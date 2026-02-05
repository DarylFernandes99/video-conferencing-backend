from app.repositories.room_repository import room_repository

class SignalingService:
    def __init__(self, repo):
        self.repo = repo

    async def join_room(self, room_id: str, user_id: str):
        await self.repo.add_user_to_room(room_id, user_id)
        members = await self.repo.get_room_members(room_id)
        # Filter out self
        peers = [m for m in members if m != user_id]
        return peers

    async def leave_room(self, user_id: str):
        room_id = await self.repo.get_user_room(user_id)
        if room_id:
            await self.repo.remove_user_from_room(room_id, user_id)
            return room_id
        return None

signaling_service = SignalingService(room_repository)
