import unittest
import time
import datetime

from squeezerp import resources
from tests import datatools_API


class TestDataTools(unittest.TestCase):

    @staticmethod
    def test_data_uploader_csv():
        path = resources.DATA_UPLOADER_PATH_CSV
        delimiter = ","
        sheet = "Categories"
        t = time.time()
        data_uploader = datatools_API.DataUploader(path=path, sheet_name=sheet, stop_option=False)
        results = data_uploader.import_csv(delimiter=delimiter, hd_option=False)
        t2 = time.time()
        t_total = t2-t
        print "time(s): ", t_total
        print data_uploader.data_shape
        print results
        print "has error: ", data_uploader.error
        print "#errors: ", data_uploader.errors_count

        for cl in range(len(results[0])):
            for c in range(len(results)):
                print results[c][cl]

    @staticmethod
    def test_data_uploader__excel():
        path = resources.DATA_UPLOADER_PATH_XLS
        sheet = "Categories"
        t = time.time()
        a = datetime.datetime.now()
        data_uploader = datatools_API.DataUploader(path=path, sheet_name=sheet, stop_option=True)
        results = data_uploader.import_excel()
        t2 = time.time()
        t_total = t2-t
        b = datetime.datetime.now()
        c = b - a
        print a, b, c
        print divmod(c.total_seconds(), 3600)[1]
        print "time(s): ", t_total
        print data_uploader.data_shape
        print results
        print "has error: ", data_uploader.error
        print "#errors: ", data_uploader.errors_count
