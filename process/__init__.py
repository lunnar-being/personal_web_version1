import os
import re
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from app import db
from disruptive import app
from app.models import PolicyText, File
from config import Config
from traceback import format_exc
from util import get_md5_str, pure_text, logging, FileName, FileNameNotMatchError, check_path

BASE_DIR = Config.BASE_DIR
RANK_TH = Config.RANK_TH
PROCESS_BASE_DIR = Config.BASE_DIR + '/process'


def path_join(path_):
    return os.path.join(app.config['BASE_DIR'], path_)
