from __future__ import absolute_import
from __future__ import print_function
import urllib

import time
import logging

logger = logging.getLogger(__name__)

from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.applications.resnet50 import preprocess_input, decode_predictions
import numpy as np


class Pipeline(object):
    """
    Takes care of running computations.
    """

    def __init__(self):
        """
        Prepare computation pipeline by loading the keras model
        """
        # load the model
        self.network = InceptionV3()

    def predict(self, url):
        logger.debug('getting {}'.format(url))
        img = image.load_img(urllib.urlretrieve(url)[0], target_size=(299, 299))
        # For faster processing, we should receive a numpy array directly, maybe
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        # Predict
        preds = self.model.predict(x)
        # Return the ImageNet class label
        return decode_predictions(preds, top=3)[0]
