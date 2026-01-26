import logging
import sys
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from nest.core import Module, PyNestFactory
from src.config.swagger_config import setup_swagger
from src.database.prisma_service import prisma_service
from src.modules.auth.auth_module import AuthModule
from src.modules.user.user_module import UserModule
from src.config.env_config import is_development
from src.core.exceptions.handlers import setup_exception_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logging.getLogger("pynest").setLevel(logging.WARNING)


@Module(imports=[AuthModule, UserModule])
class AppModule:
    pass


@asynccontextmanager
async def lifespan(_) -> AsyncGenerator[None, None]:
    # Startup
    await prisma_service.connect()
    logging.info("Started server at http://localhost:8000")
    yield
    # Shutdown
    await prisma_service.disconnect()


app = PyNestFactory.create(
    AppModule,
    description="Boilerplate PyNest Application",
    title="PyNest Application",
    version="1.0.0",
    debug=is_development,
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)


http_server = app.get_server()
setup_swagger(http_server)
setup_exception_handlers(http_server)
