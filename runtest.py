# coding=utf-8
from core import kfk_choose, savePointdata
from conf import settings

savePointdata.save_data_in_redis(settings.DATA_PATH)
kfk_choose.choose_userid_from()
