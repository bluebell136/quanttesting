# -*- coding: utf-8 -*-
"""
@Time    : 2020/2/3 下午5:52

@File    : test_readzxg.py

@author  : pchaos
@license : Copyright(C), pchaos
@Contact : p19992003#gmail.com
"""
import unittest
import os
import QUANTAXIS as qa
from userFunc import read_zxg
from userFunc import xls2zxg


class testReadZXG(unittest.TestCase):
    def test_read_zxg(self):
        """测试读取自选股列表
        """
        fn = 'zxg.txt'
        # code列表
        code = read_zxg(fn)
        if len(code) == 0:
            # 自选股为空
            self.assertTrue(not os.path.exists(fn), "找到文件：{}".format(fn))
        else:
            self.assertTrue(os.path.exists(fn), "没找到文件：{}".format(fn))
            print("自选列表：{}".format(code))

    def test_readzxg_name(self):
        """代码对应的指数名称
        """
        fn = 'zxg.txt'
        # code列表
        code = read_zxg(fn)
        data = qa.QA_fetch_index_list_adv()
        print(data.columns)
        # print(data[['code', 'name']])
        for c in code:
            print(c, data.loc[c]['name'])

    def test_xls2zxg(self):
        xlsfile = "担保品20200210.xls"
        zxgfile = "/tmp/{}.txt".format(xlsfile)
        xls2zxg(xlsfile, zxgfile)
        codes = read_zxg(zxgfile, length=15)
        self.assertTrue(len(codes) > 10, "读取数量太少：{}".format(codes))
        print(codes[:10])
        for code in codes:
            if code.startswith("159"):
                print(code)


if __name__ == '__main__':
    unittest.main()