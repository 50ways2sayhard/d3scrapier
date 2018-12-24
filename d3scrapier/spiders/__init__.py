# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.

import os
base_url = "http://db.d.163.com"


def get_current_path():
    return os.path.dirname(__file__)
