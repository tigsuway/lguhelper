from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
Other = Table('Other', post_meta,
    Column('other_id', Integer, primary_key=True, nullable=False),
    Column('document_name', String(length=100)),
    Column('description', Text),
    Column('creation_date', Date),
    Column('created_by', String(length=100)),
    Column('up_by', Integer),
    Column('filename', String(length=100)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Other'].columns['created_by'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['Other'].columns['created_by'].drop()
