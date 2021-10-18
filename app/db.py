import databases

from config import settings

DATABASE_URL = 'postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'.format(**settings.DB)
database = databases.Database(DATABASE_URL)
