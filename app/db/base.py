from app.db.session import Base

# Import all the models, so that the Base class
# has them before being imported by Alembic.
import app.models  # noqa
