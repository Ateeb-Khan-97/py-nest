import logging
import sys

from nest.core import Module, PyNestFactory
from src.config.swagger_config import setup_swagger
from src.database.prisma_service import PrismaService
from src.modules.auth.auth_module import AuthModule
from src.modules.user.user_module import UserModule
from src.config.env_config import is_development, is_production
from src.core.exceptions.handlers import setup_exception_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logging.getLogger("pynest").setLevel(logging.WARNING)


@Module(imports=[AuthModule, UserModule], providers=[PrismaService])
class AppModule:
    pass


app = PyNestFactory.create(
    AppModule,
    description="Boilerplate PyNest Application",
    title="PyNest Application",
    version="1.0.0",
    debug=is_development,
    docs_url=None,
    redoc_url=None,
)


http_server = app.get_server()
setup_swagger(http_server)
setup_exception_handlers(http_server)
