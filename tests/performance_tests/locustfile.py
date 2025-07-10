from locust import HttpUser, task


class PerfConnectionTest(HttpUser):

    @task
    def index(self):
        response = self.client.get("/")

    @task    
    def login(self):
        response = self.client.post("/showSummary", {"email": "admin@irontemple.com"})



class PerfBookTest(HttpUser):

    @task
    def bookPlaces(self):
        response = self.client.post("/showSummary", {"email": "admin@irontemple.com"})
        response = self.client.post("/purchasePlaces", {"club": "Iron Temple", "competition": "Fall Classic", "places": 2})


class PerfBoard(HttpUser):

    @task
    def board(self):
        response = self.client.get("/points")
