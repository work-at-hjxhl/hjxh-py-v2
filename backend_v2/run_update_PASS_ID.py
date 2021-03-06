import logging
from datetime import datetime

import pymongo

from pdd.PinDuoDuo import PingDuoDuoSpider
from settings import MONGO_URI, MONGO_DATABASE_NAME

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    for user in [
        ("皇家小虎食品旗舰店冯露", "Fl123456..."),
        ("牧老板食品专营店冯露", "Fl123456..."),
        ("千寻生鲜:志骐", "Hzq734985.."),
        ("牧鲜生:志骐", "Hzq706752.."),
        ("农夫牧场邓雪梅", "Dxm20201201.."),
        ("乐和食品店:冯露", "FL123456..."),
        ("老爹生鲜邓雪梅", "Dxm2021.3.18"),
    ]:

        """
        get PASS_ID
        """
        username, password = user
        pdd = PingDuoDuoSpider(username, password)
        user_info = pdd.get_pass_id()

        """
        update database
        """
        if not user_info:
            logging.warning(f"账号【{username}】 登录失败，请检查账号信息")
        else:
            client = pymongo.MongoClient(MONGO_URI)
            db = client[MONGO_DATABASE_NAME]
            coll_name = "accounts"
            db[coll_name].update_one({"_id": user_info["id"]}, {"$set": user_info}, upsert=True)
            logging.info(f"updated account of {username} into database: [{MONGO_DATABASE_NAME}, {coll_name}]")
