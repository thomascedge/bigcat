import pytest
from datetime import datetime
from uuid import uuid4
from src.concerts import service as concerts_service
from src.concerts.model import Concert, ConcertStatus
from src.exceptions import ConcertNotFoundError, ConcertCreationError, NoAdminPermissions

class TestConcertsService:
    def test_get_concert_by_id(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        
        concert = concerts_service.get_concert_by_id(test_concert.uid, db_session)
        assert concert.uid == test_concert.uid

        with pytest.raises(ConcertNotFoundError):
            concerts_service.get_concert_by_id('', db_session)
            

    def test_get_all_concerts(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        
        concerts = concerts_service.get_all_concerts(db_session)
        assert len(concerts.concert_list) > 0

    def test_search_concerts(self, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())

        query = { 
            'concert_id': test_concert.uid,
            'artist': 'TESTARTIST',
        }
    
        concerts = concerts_service.search_concerts(artist=query['artist'], db=db_session)
        
        assert len(concerts.concert_list) > 0
        assert any(concert.uid == query['concert_id'] for concert in concerts.concert_list)

        concerts = concerts_service.search_concerts(concert_id=query['concert_id'], db=db_session)
        assert len(concerts.concert_list) > 0
        assert any(concert.uid == query['concert_id'] for concert in concerts.concert_list)
    
    def test_create_concert(self, test_user, test_user_admin, test_concert, db_session):
        concert = concerts_service.create_concert(test_user_admin, test_concert, db_session)
        assert concert.uid == test_concert.uid

        with pytest.raises(ConcertCreationError):
            concerts_service.create_concert(test_user_admin, None, db_session)

        with pytest.raises(NoAdminPermissions):
            concerts_service.create_concert(test_user, test_concert, db_session)

    def test_update_concert(self, test_user, test_user_admin, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        concert_id = test_concert.uid

        concert_update = Concert(
            uid=concert_id,
            artist='TESTARTIST1',
            tour_name='TESTTOUR1',
            venue='TESTVENUE1',
            location='TESTLOCATION1',
            concert_datetime=datetime(2025, 1, 1),
            status=ConcertStatus.COMPLETED.value,
            update_datetime=datetime.now()
        )

        updated_concert = concerts_service.update_concert(test_user_admin, test_concert.uid, concert_update, db_session)
        assert updated_concert.uid == concert_id
        assert updated_concert.artist == 'TESTARTIST1'
        assert updated_concert.tour_name == 'TESTTOUR1'
        assert updated_concert.venue == 'TESTVENUE1'
        assert updated_concert.location == 'TESTLOCATION1'
        assert updated_concert.status == ConcertStatus.COMPLETED.value

        with pytest.raises(NoAdminPermissions):
            concerts_service.update_concert(test_user, test_concert.uid, concert_update, db_session)

    def test_cancel_concert(self, test_user, test_user_admin, test_concert, db_session):
        db_session['concert'].insert_one(test_concert.model_dump())
        concerts_service.cancel_concert(test_user_admin, test_concert.uid, db_session)

        concert = db_session['concert'].find_one({'uid': test_concert.uid})
        assert concert['status'] == ConcertStatus.CANCELED.value

        with pytest.raises(NoAdminPermissions):
            concerts_service.cancel_concert(test_user, test_concert.uid, db_session)
