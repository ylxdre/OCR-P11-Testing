
class TestDate:
    '''
    test the booking for the past competitions
    '''

    def test_should_not_display_book_link_for_past_competitions(self, connect):
        '''
        test that the booking link isn't displayed when competition date is older than today
        '''
        li = connect.find_all("li")
        assert not li[0].a
        assert li[1].a

    def test_forged_url_on_past_competition_should_raise_flash(self, client):
        '''
        test that a flash warning occur when trying to connect to an URL on an old competition
        '''
        url = '/book/Spring Festival/Iron Temple'
        response = client.get(url)
        assert "You cannot book for a past competition" in response.data.decode()

