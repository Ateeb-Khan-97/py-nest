import logging
from prisma import Prisma


class PrismaService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.client = Prisma(log_queries=True)

    async def connect(self):
        try:
            await self.client.connect()
            self.logger.info("Connected to database")
        except Exception as e:
            self.logger.error(f"Error connecting to database: {e}")
            raise e

    async def disconnect(self):
        try:
            await self.client.disconnect()
            self.logger.info("Disconnected from database")
        except Exception as e:
            self.logger.error(f"Error disconnecting from database: {e}")
            raise e


prisma_service = PrismaService()
