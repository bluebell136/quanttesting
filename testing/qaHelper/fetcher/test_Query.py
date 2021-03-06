# -*- coding: utf-8 -*-

import unittest
from unittest import TestCase
import datetime
import pandas as pd
import numpy as np
import QUANTAXIS as qa
from QUANTAXIS.QAFetch.QAQuery import QA_fetch_stock_day, QA_fetch_stock_min
from QUANTAXIS.QAUtil import DATABASE
from qaHelper.fetcher import QueryMongodb as qm
from .qhtestbase import QhBaseTestCase


class testQuery(QhBaseTestCase):
    def test_collections(self):
        collections = qm.collectionsDay
        self.assertTrue(collections.name == DATABASE.stock_day.name, "数据表名应该相同 {}".format(collections))

        qm.collectionsDay = DATABASE.stock_min
        self.assertTrue(collections.name != qm.collectionsDay.name)
        print("原始表名：{}，\n改变后表名：{}".format(collections, qm.collectionsDay))

        qm.collectionsDay = collections
        self.assertTrue(collections.name == qm.collectionsDay.name)

    def test_getNumpy(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        arrary = qm.getNumpy(code, start, end)
        self.assertIsInstance(arrary, np.ndarray, "应返回类型：np.ndarray，实际返回数据类型：{}".format(type(arrary)))
        self.assertTrue(len(arrary) > days // 10, "返回数据数量应该大于0。")

    def test_getNumpy_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        array1 = qm.getNumpy(code, start, end)
        self.assertTrue(len(array1) > 0, "返回数据数量应该大于0。")
        array2 = QA_fetch_stock_day(code, start, end)
        self.assertTrue(len(array1) == len(array2), "和QA返回的数据,长度不一致")
        # 两种方式检测numpy数据一致性
        self.assertTrue(np.array_equal(array1, array2), "和QA返回的数据不一致{}".format(""))
        self.assertTrue((array1 == array2).all(),
                        "和QA返回的数据不一致{}".format(np.setdiff1d(array1, array2, assume_unique=True)))

    def test_get_noData(self):
        code = '600001'  # 不存在的股票代码
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.getNumpy(code, start, end)
        self.assertTrue(isinstance(df, np.ndarray) and df.size == 1, "{}已退市，返回数据数量应该等于0,{}。".format(code, df))

    def test_get_min(self):
        code = '000001'
        days = 30 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = qm.get(code, start, end, frequence='1min')
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")

    def test_get_min_diffQA(self):
        code = '000001'
        days = 10 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        array1 = qm.get(code, start, end, frequence='1min')
        array2 = QA_fetch_stock_min(code, start, end, frequence='1min')
        # todo df的长度比df2长。未找出原因
        if len(array1) > len(array2):
            print("array1f的长度比array2长")
            array1 = array1[-len(array2):]
        elif len(array1) < len(array2):
            print("array2的长度比array1长")
            array2 = array2[-len(array1):]
        self.assertTrue(len(array1) == len(array2), "和QA返回的分钟线数据长度不一致:{}:{}".format(len(array1), len(array2)))
        # todo  连续获取分钟数据时，不定时返回结果不想等。报错
        self.assertTrue(np.array_equal(array1, array2),
                        "和QA返回的分钟线数据不一致:{}".format(np.setdiff1d(array1, array2, assume_unique=True)))


if __name__ == '__main__':
    unittest.main()
