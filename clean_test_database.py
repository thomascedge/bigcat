from src.database.core import client
from loguru import logger as clean_log

database = client['bigcat']

# delete any test users
deteled = 0
result = database['user'].delete_many({'first_name': 'Test'})
deteled += result.deleted_count
result = database['user'].delete_many({'first_name': 'New'})
deteled += result.deleted_count
clean_log.info(f"Deleted {deteled} users documents.")

# delete any test concerts
result = database['concert'].delete_many({'concert_id': {'$regex': 'TEST', '$options': 'i'}})
clean_log.info(f"Deleted {result.deleted_count} concert documents.")

# delete any test seats
result = database['seat'].delete_many({'concert_id': {'$regex': 'TEST', '$options': 'i'}})
clean_log.info(f"Deleted {result.deleted_count} seats documents.")

# detele any test bookings
result = database['booking'].delete_many({'concert_id': {'$regex': 'TEST', '$options': 'i'}})
clean_log.info(f"Deleted {result.deleted_count} bookings documents.")
