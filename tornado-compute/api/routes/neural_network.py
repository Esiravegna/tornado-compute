from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import tornado.web
import tornado.gen
import dualprocessing
import logging
import json


class NeuralNetwork(tornado.web.RequestHandler):
    """
    POST a URL of an image to this address to run it through the model
    """

    def initialize(self, broker):
        """
        The initialization
        :param broker: a dualprocessing brjer
        """
        self.broker = broker

    def get(self):
        self.render('..//templates/vgg.html')

    @tornado.gen.coroutine
    def post(self):
        try:
            url = self.get_argument("url", None)
            base64_encoded = self.get_argument("base64_encoded", None)
            call = dualprocessing.AsyncCall("predict", url=url, base64_encoded=base64_encoded)
            response = yield self.broker.submit_call_async(call)
            if response.success:
                self.write({'data' :[{u'label': a_result[1], u'proba': str(a_result[2])} for a_result in response.result]})
            else:
                raise response.error
        except:
            def lastExceptionString():
                exc_type, ex, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                return "{0} in {1}:{2}".format(ex, fname, exc_tb.tb_lineno)

            exmsg = lastExceptionString()
            logging.critical(exmsg)
            self.write(exmsg)
