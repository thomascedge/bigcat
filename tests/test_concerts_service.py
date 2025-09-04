import pytest
from datetime import datetime
from src.concerts import service as concerts_service
from src.concerts.model import Concert, ConcertStatus
from src.exceptions import ConcertNotFoundError

class TestConcertsService:
    def test_get_concert_by_id(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        
        concert = concerts_service.get_concert_by_id(test_concert.concert_id, db_session)
        assert concert.concert_id == test_concert.concert_id

    def test_get_all_concerts(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        
        concerts = concerts_service.get_all_concerts(db_session)
        assert len(concerts.concert_list) > 0

    def test_search_concerts(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())

        query = { 
            'concert_id': 'TESTCONCERT',
            'artist': 'TESTARTIST',
            # 'tour_name': 'TESTTOUR',
            # 'venue': 'TESTVENUE',
            # 'location': 'TESTLOCATION',
            # 'date': datetime(2025, 1, 1)
        }
    
        concerts = concerts_service.search_concerts(artist=query['artist'], 
                                                    # tour_name=query['tour_name'], 
                                                    # venue=query['venue'],
                                                    # location=query['location'],
                                                    # date=query['date'],
                                                    db=db_session)
        
        assert len(concerts.concert_list) > 0
        assert concerts.concert_list[0].concert_id == query['concert_id']

        concerts = concerts_service.search_concerts(concert_id=query['concert_id'], db=db_session)
        assert len(concerts.concert_list) > 0
        assert concerts.concert_list[0].concert_id == query['concert_id']
    
    def test_create_concert(self, test_concert, db_session):
        concert = concerts_service.create_concert(test_concert, db_session)
        assert concert.concert_id == test_concert.concert_id

        with pytest.raises(ConcertNotFoundError):
            concerts_service.get_concert_by_id('', db_session)

    def test_update_concert(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        concert_update = Concert(
            concert_id='TESTCONCERT1',
            artist='TESTARTIST1',
            tour_name='TESTTOUR1',
            venue='TESTVENUE1',
            location='TESTLOCATION1',
            datetime=datetime(2025, 1, 1),
            status=ConcertStatus.COMPLETED.value
        )

        updated_concert = concerts_service.update_concert(test_concert.concert_id, concert_update, db_session)
        assert updated_concert.concert_id == 'TESTCONCERT1'
        assert updated_concert.artist == 'TESTARTIST1'
        assert updated_concert.tour_name == 'TESTTOUR1'
        assert updated_concert.venue == 'TESTVENUE1'
        assert updated_concert.location == 'TESTLOCATION1'
        assert updated_concert.status == ConcertStatus.COMPLETED.value

    def test_cancel_concert(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        concerts_service.cancel_concert(test_concert.concert_id, db_session)

        concert = db_session['concert'].find_one({'concert_id': test_concert.concert_id})
        assert concert['status'] == ConcertStatus.CANCELED.value
