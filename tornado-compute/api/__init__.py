from __future__ import print_function

from routes.neural_network import NeuralNetwork
from tornado.web import Application
from dualprocessing import Broker
import logging

logger = logging.getLogger(__name__)


def app_factory(network_factory):
    """
    creates a tornado App
    :param network_factory: (function) a method called for the dualprocessor broker that creates the network in memory
    :return:
    """
    logger.info("Starting computation broker...")
    broker = Broker(network_factory)
    endpoints = [
        (r"/net", NeuralNetwork, dict(broker=broker))
    ]
    logger.info("Starting service...")
    app = Application(endpoints)
    return app
