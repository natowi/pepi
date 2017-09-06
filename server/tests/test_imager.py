import numpy
import os
import glob
import time
import imghdr

import pytest
from PIL import Image


# noinspection PyMethodMayBeStatic
class MetaImagerContract(object):
    @pytest.fixture(scope="module")
    def concrete_imager(self):
        raise NotImplementedError('You must override the @pytest.fixture `server`')

    def test_still(self, concrete_imager):
        image = concrete_imager.still()
        assert isinstance(image, numpy.ndarray)
        for x in image:
            for y in x:
                assert all([0 <= c <= 255 for c in y])

    def test_stream_jpg_to_folder(self, concrete_imager, tmpdir):
        path = str(tmpdir)
        concrete_imager.stream_jpg_to_folder(path)
        time.sleep(3)
        concrete_imager.stop_streaming()

        for file_ in glob.glob(path + '/*'):
            name, extension = os.path.splitext(file_)
            assert extension == '.jpg' or extension == '.jpeg'
            assert imghdr.what(file_) == 'jpeg'
            try:
                image = Image.open(file_)
                assert image.format == 'JPEG'
            except IOError as e:
                pytest.fail('Couldn\'t open the image (malformed?) at file {}. Exception : {}'.format(file_, e), True)

    def test_stopping_thread(self, concrete_imager):
        concrete_imager.stop_streaming()
        time.sleep(0.5)
        concrete_imager.stop_streaming()