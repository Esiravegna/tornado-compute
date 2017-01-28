from locust import HttpLocust, TaskSet

def medium_image(l):
    l.client.post("/net", {"url": "http://mynameismichelle.com/wp-content/uploads/2014/05/tardis.png"})

def large_image(l):
    l.client.post("/net", {"url": "http://www.ex-astris-scientia.org/scans/other/enterprise-tvguide-oblique.jpg"})


class StressTest(TaskSet):
    tasks = {large_image:2, medium_image:1}


class WebsiteUser(HttpLocust):
    task_set = StressTest
    min_wait = 5000
    max_wait = 9000