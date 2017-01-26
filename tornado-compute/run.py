import logging
from tornado.ioloop import IOLoop

from api import app_factory

logger = logging.getLogger(__name__)


def pipeline_factory():
    from core.pipeline import Pipeline
    return Pipeline()


if __name__ == "__main__":
    logging.info("Starting service...")
    app = app_factory(pipeline_factory())
    port = 2017
    app.listen(port)
    logging.info("Service is running publicly. at http://{0}:{1}/".format("[host-IP]", port))
    logging.warn(
        "WARNING: Do not use multiple tabs in the same browser to test! The browser will delay sending of the second request until the first one returned! (Reference: http://www.tornadoweb.org/en/stable/faq.html)")
    IOLoop.current().start()

    logging.info("Ended.")
