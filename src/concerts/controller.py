# @app.get('/concert')
# async def search_concerts(artist: str|None=None, venue: str|None=None, date: str|None=None, concert_id: str|None=None):
#     """
#     Searches database for concert data based on given query. It is assumed that a concert_id
#     will not be searched with an artist, venue, or date.
#     Example query: /concert/?artist=Juliana+Huxtable&date=2025-09-05T22:30:00

#     :param optional str artist: artist name
#     :param optional str venue: venue name
#     :param optional datetime datetime: datetime object
#     :return: list of concerts object
#     :raises: 404 error if concert not found
#     """
#     concert_list = []

#     if concert_id:
#         query = {'concert_id': concert_id}
#     else:
#         # format date to datetime and get date range for querying
#         if date:
#             start_date = datetime.strptime(f'{date} 00:00', '%m-%d-%Y %H:%M')
#             end_date = datetime.strptime(f'{date} 23:59', '%m-%d-%Y %H:%M')
        
#         if artist and venue and date:
#             query = {'$and': [{'artist': {'$regex': artist, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}, {'datetime': {"$gte": start_date, "$lte": end_date}}]}
#         elif artist and venue and not date:
#             query = {'$and': [{'artist': {'$regex': artist, '$options': 'i'}}, {'venue': {'$regex': venue, '$options': 'i'}}]}
#         elif artist and not venue and date:
#             query = {'$and': [{'artist': {'$regex': artist, '$options': 'i'}}, {'datetime': {"$gte": start_date, "$lte": end_date}}]}
#         elif not artist and venue and date:
#             query = {'$and': [{'venue': {'$regex': venue, '$options': 'i'}}, {'datetime': {"$gte": start_date, "$lte": end_date}}]}
#         elif artist and not venue and not date:
#             query = {'artist': {'$regex': artist, '$options': 'i'}}
#         elif not artist and venue and not date:
#             query = {'venue': {'$regex': venue, '$options': 'i'}}
#         elif not artist and not venue and date:
#             query = {'date': date}
        
#     for record in CONCERT_DB.find(query):
#         concert_list.append(Concert(**record))

#     if len(concert_list) != 0:
#         return concert_list
#     else:
#         raise HTTPException(status_code=404, detail='No concerts found.')