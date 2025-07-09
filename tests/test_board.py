from bs4 import BeautifulSoup
from server import loadClubs


class TestBoardDisplayPoints:

    def test_should_get_200(self, client):
        '''
        test if the page is retrieved
        '''
        response = client.get('/points')
        assert response.status_code == 200

    def test_should_display_right_size_list(self, client):
        '''
        test if the list of club displayed and in DB have the same size 
        '''
        list_club = loadClubs()
        response = client.get('/points')
        soup = BeautifulSoup(response.data, "html.parser")
        li = soup.find_all("li")
        assert len(li) == len(list_club)


