import os
import time
import sys
from dotenv import load_dotenv
from datetime import datetime
from model import *
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from tqdm import tqdm

def haim_austin_dates():
    # create seats
    seats_list = []
    moody_floor_sections_list = ['1', '2', '3']
    moody_first_sections_list = ['106', '107', '108', '109', '110', '111', '112', 
                                '113', '114', '115', '116', '117', '118', '119']
    moody_second_sections_list = ['120', '210', '211', '212', '213', '214', '215']

    # GA
    for _ in range(500):
        seat = Seat(
            concert_id='HAIMATX2025',
            seat_number='GA',
            seat_type=2,
            price=53.00,
            status=0,
        )
        seats_list.append(seat)

    # floor 1-3 -> FLR3 R6 S6 -> 29x22
    for section in moody_floor_sections_list:
        for row in range(1, 30):
            for seat in range(1, 23):
                seat = Seat(
                    concert_id='HAIMATX2025',
                    seat_number=f'FLR{section} R{row} S{seat}',
                    seat_type=1,
                    price=46.00,
                    status=0,
                )
                seats_list.append(seat)

    # sections -> SEC104 RG S16
    for section in moody_first_sections_list:
        for row in range(ord('A'), ord('X')):
            for seat in range(1, 19):
                seat = Seat(
                    concert_id='HAIMATX2025',
                    seat_number=f'SEC{section} R{chr(row)} S{seat}',
                    seat_type=0,
                    price=35.00,
                    status=0,
                )
                seats_list.append(seat)

    for section in moody_second_sections_list:
        for row in range(ord('A'), ord('X')):
            for seat in range(1, 19):
                seat = Seat(
                    concert_id='HAIMATX2025',
                    seat_number=f'SEC{section} R{chr(row)} S{seat}',
                    seat_type=0,
                    price=20.00,
                    status=0,
                )
                seats_list.append(seat)

    # create concert
    concert = Concert(
        concert_id='HAIMATX2025',
        artist='HAIM',
        tour_name='I quit tour 2025',
        venue='Moody Center ATX',
        location='Austin, TX, USA',
        datetime=datetime(2025, 9, 26, 19, 30, 0),
    )

    return concert, seats_list

def haim_houston_dates():
    seats_list = []

    # premium
    for _ in range(600):
        seat = Seat(
            concert_id='HAIMHTX2025',
            seat_number='GA',
            seat_type=0,
            price=53.00,
            status=0,
        )
        seats_list.append(seat)

    # vip
    for _ in range(200):
        seat = Seat(
            concert_id='HAIMHTX2025',
            seat_number='GA',
            seat_type=2,
            price=72.25,
            status=0,
        )
        seats_list.append(seat)

    # regular
    for _ in range(3000):
        seat = Seat(
            concert_id='HAIMHTX2025',
            seat_number='GA',
            seat_type=0,
            price=20.00,
            status=0,
        )
        seats_list.append(seat)

    # create concert
    concert = Concert(
        concert_id='HAIMHTX2025',
        artist='HAIM',
        tour_name='I quit tour 2025',
        location='Houston, TX, USA',
        venue='White Oak Music Hall Lawn',
        datetime=datetime(2025, 9, 28, 18, 30, 0),
    )

    return concert, seats_list

def juliana_austin_dates():
    seats_list = []

    # premium
    for _ in range(600):
        seat = Seat(
            concert_id='SERAPHIMATX2025',
            seat_number='GA',
            seat_type=0,
            price=20.00,
            status=0,
        )
        seats_list.append(seat)

    # create concert
    concert = Concert(
        concert_id='SERAPHIMATX2025',
        artist='Juliana Huxtable, Lucia Beyond',
        tour_name='Seraphim Presents: Juliana Huxtable',
        location='Austin, TX, USA',
        venue='Kingdom',
        datetime=datetime(2025, 9, 5, 22, 30, 0),
    )

    return concert, seats_list

def magdelena_bay_austin_dates():
    seats_list = []

    for _ in range(1700):
        seat = Seat(
            concert_id='MAGBAYATX2025',
            seat_number='GA',
            seat_type=0,
            price=63.20,
            status=0,
        )
        seats_list.append(seat)

    # create concert
    concert = Concert(
        concert_id='MAGBAYATX2025',
        artist='Magdelena Bay',
        tour_name='Official 2025 ACL Fest Nights: Magdalena Bay',
        location='Austin, TX, USA',
        venue="Emo's Austin",
        datetime=datetime(2025, 10, 10, 21, 00, 0),
    )

    return concert, seats_list

def wolf_alice_austin_dates():
    seats_list = []

    for _ in range(1700):
        seat = Seat(
            concert_id='WOLFALICE2025',
            seat_number='GA',
            seat_type=0,
            price=41.90,
            status=0,
        )
        seats_list.append(seat)

    # create concert
    concert = Concert(
        concert_id='WOLFALICE2025',
        artist='Wolf Alice',
        tour_name='Wolf Alice North American Tour 2025',
        location='Austin, TX, USA',
        venue="Emo's Austin",
        datetime=datetime(2025, 9, 30, 19, 00, 0),
    )

    return concert, seats_list

def _create_record(db, data):
    for record in data:
        yield db.insert_one(record.__dict__)

if __name__ == '__main__':
    # aggregate all concerts and seats
    concerts = []
    seats = []
    items_list = [haim_austin_dates(), haim_houston_dates(), juliana_austin_dates(), magdelena_bay_austin_dates(), wolf_alice_austin_dates()]
    # items_list = [juliana_austin_dates()]

    for items in items_list:
        concert, seats_list = items
        concerts.append(concert)
        seats.extend(seats_list)
    
    # get password and uri for database connection
    load_dotenv()
    db_password = os.getenv('MONGO_PASSWORD')
    uri = os.getenv('DATABASE_URI').replace('db_password', db_password)

    # create client and connect to server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # ping for confirmation and update databases
    try:
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")

        db = client['bigcat']

        CONCERT_CLUSTER = db['concert']
        SEAT_CLUSTER = db['seat']

        # populate concerts    
        for _ in tqdm(_create_record(CONCERT_CLUSTER, concerts), desc='Populating bigcat.concert database.', bar_format='[{elapsed}<{remaining}] {n_fmt}/{total_fmt} | {l_bar}{bar} {rate_fmt}{postfix}', colour='yellow'):
            time.sleep(0.01)

        # populate seats
        for _ in tqdm(_create_record(SEAT_CLUSTER, seats), desc='Populating bigcat.seat database.', bar_format='[{elapsed}<{remaining}] {n_fmt}/{total_fmt} | {l_bar}{bar} {rate_fmt}{postfix}', colour='red'):
            time.sleep(0.01)

        print('Database successfully populated')

    except Exception as e:
        print('\n------- ERROR ------')
        print(e)
        print('--------------------\n')
