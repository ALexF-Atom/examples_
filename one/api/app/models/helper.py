import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg
from app.models.base import Base


class ModelHelper(Base):
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    ...

    # helper_event_key_id = sa.Column(sa.ForeignKey('model_event_key.id',
    #                                        ondelete='SET NULL'))

