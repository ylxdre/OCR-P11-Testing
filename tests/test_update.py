
class TestPointsUpdate:

    def test_should_not_be_ok_the_second_time(self, connect, client, club2):
        '''
        this books an amount of points-1 places
        then test if 1 points remains displayed on page
        '''
        points = int(connect.span.text)
        club2.update({"places": points-1})
        response = client.post('/purchasePlaces', data=club2)
        assert f"Great ! {points-1} places booked for {club2['competition']}" in response.data.decode()
