from typing import List
from nest.core import Injectable
from prisma.models import Users
from prisma.types import UsersCreateInput, UsersUpdateInput, UsersWhereInput

from src.core.services import PrismaService


@Injectable()
class UserService:

    def __init__(self, db: PrismaService):
        pass

    async def find_one_by_id(self, id: int) -> Users | None:
        return await self.db.users.find_first(where={"id": id})

    async def find_one_by_email(self, email: str) -> Users | None:
        return await self.db.users.find_first(where={"email": email})

    async def find_one_by(self, where: UsersWhereInput) -> Users | None:
        return await self.db.users.find_first(where=where)

    async def create(self, user: UsersCreateInput) -> Users:
        return await self.db.users.create(data=user)

    async def update(self, id: int, user: UsersUpdateInput) -> Users:
        return await self.db.users.update(where={"id": id}, data=user)

    async def find_all(self) -> List[Users]:
        return await self.db.users.find_many()
