from src.database.core import client
from loguru import logger as clean_log

database = client['bigcat']

# delete any test users
result = database['user'].delete_many({'first_name': 'Test'})
clean_log.info(f"Deleted {result.deleted_count} users documents.")

# delete any test bookings
# result = database['booking'].delete_many({'concert_id': 'TESTCONCERT'})
# clean_log.info(f"Deleted {result.deleted_count} users documents.")