#!/usr/bin/env python
# -*- coding=utf-8 -*-
"""
# author: linyl
# Date: 2019-07-31 15:44:22
# Description: 
"""
from sqlalchemy import Column, String, Integer, create_engine, DateTime, DECIMAL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
from config import DB_URL
    
# engine = create_engine(DB_URL, echo=True)

# 创建对象的基类：
Base = declarative_base()

engine = create_engine(DB_URL, echo=True)
metadata = Base.metadata
Session = sessionmaker(bind=engine)
# session = Session()

class IPProxy(Base):
    """ip代理资源表"""
    __tablename__ = 'ip_proxy'

    # 表的结构
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(128), nullable=False, index=True, comment="代理ip")
    port = Column(String(32), nullable=False, comment="代理端口")
    procotol = Column(String(32), nullable=False, comment="代理协议")
    status = Column(String(64), nullable=False, default='normal', comment="代理状态")
    build_time = Column(DateTime, default=datetime.datetime.now, comment="创建时间")
    source = Column(String(128), comment="代理ip来源")

    def __repr__(self):
        return f"""<IPProxy(ip='{self.ip}', port='{self.port}', status='{self.status}',
         build_time='{self.build_time}')>"""


class LouPan(Base):
    """楼盘信息"""
    __tablename__ = 'loupan'

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(256), primary_key=True, nullable=False, index=True, comment='楼盘详情url')
    price = Column(DECIMAL(9, 4), nullable=False, default=0.00, comment="售价")
    pic_url = Column(String(256), comment="楼盘图片url")
    area = Column(String(128), comment="所在区域")
    city = Column(String(64), comment="城市")
    address = Column(String(256), comment="地址")
    room_type = Column(String(64), comment="居室类型")
    floor_area = Column(String(128), comment="户型面积")
    comment_num = Column(Integer, default=0, comment="评论数")
    name = Column(String(256), nullable=False, index=True)
    tag = Column(String(256))
    status = Column(String(64), nullable=False, default='normal')
    build_time = Column(DateTime, default=datetime.datetime.now)


if __name__ == "__main__":
    # engine = create_engine('mysql+mysqldb://spider:spider123@120.79.248.110:3306/spiderdb')
    # engine = create_engine(DB_URL, echo=True)
    metadata.drop_all(engine)
    metadata.create_all(engine)
    # ip_test = IPProxy(ip='127.0.0.1', port='1087', procotol='http', source="测试")
    session = Session()
    # session.add(ip_test)
    session.commit()

    proxy = session.query(IPProxy).filter(IPProxy.ip == '127.0.0.1',
                     IPProxy.port=='1087').one_or_none()
    # print(proxy.ip)




