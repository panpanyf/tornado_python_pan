# coding:utf-8

import logging
import config

from .BaseHandler import BaseHandler
from utils.image_storage import storage
from utils.common import require_logined
from utils.response_code import RET

class AvatarHandler(BaseHandler):
    """头像"""
    @require_logined
    def post(self):
        user_id = self.session.data["user_id"]
        try:
            avatar = self.request.files["avatar"][0]["body"]
        except Exception as e:
            logging.error(e)
            return self.write(dict(errno=RET.PARAMERR, errmsg="参数错误"))
        try:
            img_name = storage(avatar)
        except Exception as e:
            logging.error(e)
            img_name = None
        if not img_name:
            return self.write({"errno":RET.THIRDERR, "errmsg":"qiniu error"})
        try:
            ret = self.db.execute("update ih_user_profile set up_avatar=%s where up_user_id=%s", img_name, user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno":RET.DBERR, "errmsg":"upload failed"})
        img_url = config.image_url_prefix + img_name
        self.write({"errno":RET.OK, "errmsg":"OK", "url":img_url})


class NameHandler(BaseHandler):

    @require_logined
    def post(self):
        user_id = self.session.data["user_id"]
        user_name = self.get_argument("name")

        if user_name:
            try:
                self.db.execute("update ih_user_profile set up_name=%(name)s where up_user_id=%(id)s",name=user_name,id=user_id)
            except Exception as e:
                logging.error(e)

        try:
            res = self.db.get("select count(*) counts from ih_user_profile where up_name=%(name)s", name=user_name)
        except Exception as e:
            logging.error(e)
        else:
            if 0 != res['counts']:
                return self.write({"errno":RET.DATAEXIST, "errmsg":"该用户名已存在"})
        try:
            self.session=Session(self)
            self.session.data['user_id'] = user_id
            self.session.data["name"] = user_name
        except Exception as e:
            logging.error(e)
        self.write({"errno":RET.OK, "errmsg":"OK"})
        