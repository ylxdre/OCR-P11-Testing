from tests import conftest
from server import loadClubs
from bs4 import BeautifulSoup

class TestBoardPointsUpdate:

    def test_should_board_be_updated_after_booking(self, client):
        '''
        test if the board is well displayed, and retrive points displayed for first club
        then connect with this club email and book places
        then check on board if the balance reflect the points decrease
        '''
        nb_places = 10
        data = { 
                "competition": "Fall Classic", 
                "club": "Simply Lift",
                "places": nb_places,
                }   
        list_club = loadClubs()
        # connect on board and check if points for first club are equal to points in DB (json)
        response = client.get('/points')
        soup = BeautifulSoup(response.data, "html.parser")
        points1 = soup.find(id='points').text
        assert response.status_code == 200
        assert points1 == list_club[0]['points']
        # then connect with mail of first club
        connect = client.post('/showSummary', data={"email":"john@simplylift.co"})
        assert connect.status_code == 200
        # then book places
        response = client.post('purchasePlaces', data=data)
        assert f"Great ! "+str(nb_places)+" places booked for "+data['competition'] in response.data.decode()
        # then check points on board
        check_board = client.get('/points')
        soup = BeautifulSoup(check_board.data, "html.parser")
        points = soup.find(id='points').text
        assert int(points) == int(points1)-10
