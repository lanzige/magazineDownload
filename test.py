#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Author duzy
# @Time      : 2020/2/22 8:50
# @Author    : duzy
# @File      : test.py
# @Software  : PyCharm
class Base:
    def __init__(self):
        print('Base.__init__')


class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')


class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')


class C(Base):
    def __init__(self):
        super().__init__()
        print('C.__init__')


class D(A, C, B):
    def __init__(self):
        super().__init__()  # 等同于 super(D, self).__init__()
        print('D.__init__')


D()

print(D.mro())