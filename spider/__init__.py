import os
import re
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from app import db
from app.models import PolicyText, File
from config import Config
from traceback import format_exc

from util import get_md5_str, pure_text, logging, check_path, FileName

BASE_DIR = Config.BASE_DIR
SPIDER_BASE_DIR = BASE_DIR + '/spider'
