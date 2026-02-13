import asyncio
import logging
from nest.core import Injectable
from prisma import Prisma

from src.config.env_config import is_production


@Injectable()
class PrismaService(Prisma):
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__(log_queries=not is_production)
        asyncio.create_task(self.on_module_init())

    async def on_module_init(self):
        try:
            await self.connect()
            self.logger.info("Connected to database")
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise e
