from __future__ import absolute_import
from __future__ import print_function
import urllib
import base64
import time
import logging
from keras.applications.inception_v3 import InceptionV3
from keras.preprocessing import image
from keras.applications.inception_v3 import preprocess_input, decode_predictions
import numpy as np
from PIL import Image
from io import BytesIO

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class Pipeline(object):
    """
    Takes care of running computations.
    """

    def __init__(self, target_size=(299, 299)):
        """
        Prepare computation pipeline by loading the keras model
        """
        # load the model
        start = time.time()
        logger.info('Initia0lizing network')
        self.network = InceptionV3()
        logger.debug('took {}s'.format(time.time() - start))
        self.target_size = target_size

    def predict(self, url, base64_encoded=None):
        start = time.time()
        if not base64_encoded:
            logger.debug('getting {}'.format(url))
            img = image.load_img(urllib.urlretrieve(url)[0], target_size=self.target_size)
            logger.debug('took {}s'.format(time.time() - start))
            # For faster processing, we should receive a numpy array directly, maybe
            # This may be an async blocker, as we need to write the image to the disk?

        else:
            logger.debug('retrieving base64')
            start = time.time()
            img = self.__img_from_base64(base64_encoded)
            logger.debug('took {}s'.format(time.time() - start))
        start = time.time()
        logger.debug('Preprocessing {}'.format(url))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        logger.debug('took {}s'.format(time.time() - start))
        # Predict
        start = time.time()
        logger.debug('Predicting {}'.format(url))
        preds = self.network.predict(x)
        logger.debug('took {}s'.format(time.time() - start))
        # Return the ImageNet class label
        return decode_predictions(preds, top=3)[0]

    def __img_from_base64(self, buffer):
        """
        PIL Image resized from base64
        :param buffer: base64 encoded image
        :return: a pil image
        """
        im = Image.open(BytesIO(base64.b64decode(buffer)))
        im = im.convert('RGB')
        return im.resize(self.target_size)
