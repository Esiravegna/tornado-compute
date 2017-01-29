from locust import HttpLocust, TaskSet
import base64
import urllib

BASE_IMAGE = "http://mynameismichelle.com/wp-content/uploads/2014/05/tardis.png"
B64ENCODED_IMG = base64.b64encode(open(urllib.urlretrieve(BASE_IMAGE)[0], "rb").read())


def medium_image(l):
    l.client.post("/net", {"url": "http://mynameismichelle.com/wp-content/uploads/2014/05/tardis.png"})


def large_image(l):
    l.client.post("/net", {"url": "http://www.ex-astris-scientia.org/scans/other/enterprise-tvguide-oblique.jpg"})


def base_64_encoded(l):
    l.client.post("/net", {"base64_encoded": "{}".format(B64ENCODED_IMG)})


class StressTest(TaskSet):
    tasks = {base_64_encoded: 1}


class WebsiteUser(HttpLocust):
    task_set = StressTest
    min_wait = 5000
    max_wait = 9000
