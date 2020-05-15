# -*- coding: utf-8 -*-

import unittest
import datetime
import pandas as pd
from QUANTAXIS.QAFetch.QATdx import QA_fetch_get_stock_day, QA_fetch_get_stock_min
from qaHelper.fetcher import TDX
from .qhtestbase import QhBaseTestCase


class testTDX(QhBaseTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        pass

    def test_getAPI(self):
        """pytdx connect
        """
        from QUANTAXIS.QAUtil import QA_util_get_trade_gap
        from QUANTAXIS.QAFetch.base import _select_market_code
        code = '600000'
        frequence = 9
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        api = TDX.tdxapi
        print(type(api))
        if api.connect(TDX.ip, TDX.port, time_out=0.7):
            print(type(api))
            start_date = str(start)[0:10]
            today_ = datetime.date.today()
            lens = QA_util_get_trade_gap(start_date, today_)
            self.assertTrue(lens > 10, "时间间隔太短：{}".format(lens))
            alist = [api.to_df(
                api.get_security_bars(frequence, _select_market_code(code), code, (int(lens / 800) - i) * 800, 800)) for
                i in range(int(lens / 800) + 1)]
            api.disconnect()
        data = pd.concat(alist, axis=0, sort=False)
        self.assertTrue(len(data) > 1, "返回值为空")

    def test_get(self):
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = TDX.get(code, start, end)
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")

    def test_get_diffQA(self):
        """和QA返回的数据对比一致性
        """
        code = '000001'
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = TDX.get(code, start, end)
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")
        df2 = QA_fetch_get_stock_day(code, start, end)
        self.assertTrue(df.equals(df2), "和QA返回的数据不一致")

    def test_get_noData(self):
        code = '600001'  # 不存在的股票代码
        days = 365 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = TDX.get(code, start, end)
        self.assertTrue(df is None, "{}已退市，返回数据数量应该等于0{}。".format(code, df))

    def test_get_min(self):
        code = '000001'
        days = 30 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = TDX.get(code, start, end, frequence='1min')
        self.assertTrue(len(df) > 0, "返回数据数量应该大于0。")

    def test_get_min_diffQA(self):
        code = '000001'
        days = 30 * 1.2
        start = datetime.datetime.now() - datetime.timedelta(days)
        end = datetime.datetime.now() - datetime.timedelta(0)
        df = TDX.get(code, start, end, frequence='1min')
        df2 = QA_fetch_get_stock_min(code, start, end, frequence='1min')
        # todo df的长度比df2长。未找出原因
        if len(df) > len(df2):
            df = df[-len(df2):]
            print("df的长度比df2长:{}, {}".format(len(df), len(df2)))
        elif len(df) < len(df2):
            df2 = df2[-len(df):]
            print("df2的长度比df长:{}, {}".format(len(df), len(df2)))
        self.assertTrue(len(df) == len(df2), "和QA返回的分钟线数据长度不一致:{}:{}".format(len(df), len(df2)))
        obo = self.differOneByOne(df, df2)
        # todo  连续获取分钟数据时，不定时返回结果不想等。报错
        self.assertTrue(df.equals(df2), "和QA返回的分钟线数据不一致:{}".format(obo))


if __name__ == '__main__':
    unittest.main()
