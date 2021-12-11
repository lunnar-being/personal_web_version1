from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, DateTime, text, JSON, TIMESTAMP, CHAR, INTEGER, TEXT, VARCHAR, FLOAT, BOOLEAN
from sqlalchemy.dialects.mysql import (TINYINT)
from flask_login import UserMixin
from app import db


class Permissions:
    MANAGE_USER = 0  # 管理用户功能
    MANAGE_CONTENT = 1  # 管理内容功能
    READ = 2  # 普通浏览功能


class Roles:
    SUPER = 0
    ADMIN = 1
    COMMON = 2

    def get_role_id(self, role):
        """role as string"""
        return self.__getattribute__(role.upper())


class User(UserMixin, db.Model):
    """
    系统用户
    2 普通用户
    1 管理员
    0 超级管理员
    """
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column(INTEGER, primary_key=True)
    username = Column(TEXT, nullable=False)
    password_hash = Column(TEXT, nullable=False)
    role_id = Column(INTEGER, nullable=False)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        if self.role_id == Roles.SUPER:
            return True
        elif self.role_id == Roles.ADMIN:
            return permission in (Permissions.READ, Permissions.MANAGE_CONTENT)
        elif self.role_id == Roles.COMMON:
            return permission == Permissions.READ

    def __repr__(self):
        return "<User {}>".format(self.id)


class File(db.Model):
    """文件"""
    __tablename__ = 'file'
    __table_args__ = {'extend_existing': True}

    id = Column(INTEGER, primary_key=True)  # 文件id，主键
    filetype = Column(TINYINT)  # 文件类别: 1 origin, 2 format, 3 trans, 4 checked
    name = Column(TEXT)  # 原始文件名
    savename = Column(TEXT)  # 保存文件名称 get_md5_str(policy_text.file_url)
    extension = Column(CHAR(5), nullable=False)  # 文件类型 txt, html, pdf
    size = Column(VARCHAR(20), server_default=text("'0'"))  # 文件大小
    create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))  # 上传时间
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))  # 修改时间
    download = Column(INTEGER, server_default=text("'0'"))  # 下载次数
    extra_info = Column(JSON, server_default=text("'null'"))  # 其他信息

    def __repr__(self):
        return f"<File {self.id} {self.savename}>"


class PolicyText(db.Model):
    """
    政策
    """
    __tablename__ = 'policy_text'
    __table_args__ = {'extend_existing': True}

    id = Column(INTEGER, primary_key=True)  # 政策文本id，主键
    source_url = Column(TEXT, nullable=False)  # 来源url
    site = Column(VARCHAR(100))  # 站点（域名）
    nation = Column(VARCHAR(30), nullable=False)  # 国别
    release_time = Column(DateTime, nullable=False)  # 发布时间
    institution = Column(TEXT)  # 发布机构
    translated_institution = Column(VARCHAR(100))  # 翻译后的发布机构
    field = Column(VARCHAR(100))  # 领域
    norm_field = Column(JSON)  # 计算后的领域
    correct_field = Column(TEXT)  # 人工审核后的领域
    language = Column(VARCHAR(50), nullable=False)  # 原始语种
    keywords = Column(TEXT)  # 关键词
    old_keywords = Column(TEXT)  # 关键词
    tech_word = Column(TEXT)  # 技术词
    tech_word_list = Column(JSON)  # 技术词列表
    translated_keywords = Column(TEXT)  # 翻译后的关键词
    original_title = Column(TEXT, nullable=False)  # 原始标题
    translated_title = Column(TEXT)  # 中文标题
    abstract = Column(TEXT)  # 摘要
    translated_abstract = Column(TEXT)  # 翻译后的摘要
    file_url = Column(TEXT)  # 文件来源url
    original_file = Column(db.ForeignKey('file.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)  # 原始版本文件id
    format_file = Column(db.ForeignKey('file.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)  # 原始版本文件id
    translated_file = Column(db.ForeignKey('file.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)  # 机翻版本文件id
    checked_file = Column(db.ForeignKey('file.id', ondelete='CASCADE', onupdate='CASCADE'), index=True)  # 审校版本文件id
    use = Column(BOOLEAN)  # 是否使用
    recommend = Column(BOOLEAN)
    rank = Column(FLOAT)  # 评分
    spider_condition = db.Column(INTEGER)  # 0 pdf, 1 html
    doc_type = db.Column(VARCHAR(20))  # 'report', 'strategy', ''
    create_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))  # 上传时间
    update_time = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))  # 修改时间
    modified_by = Column(TEXT)  # 上次被xxx修改
    # 准备新增：
    # 爬虫信息，翻译后的摘要、关键词、机构
    # md5值、原始机构

    original_file_rl = db.relationship('File', foreign_keys=[original_file])
    format_file_rl = db.relationship('File', foreign_keys=[format_file])
    translated_file_rl = db.relationship('File', foreign_keys=[translated_file])
    checked_file_rl = db.relationship('File', foreign_keys=[checked_file])

    def __repr__(self):
        return f"<PolicyText {self.id} {self.site}>"


class News(db.Model):
    """
    新闻
    """
    __tablename__ = 'news'
    __table_args__ = {'extend_existing': True}

    id = Column(INTEGER, primary_key=True)  # 新闻id，主键
    title = Column(TEXT, nullable=False)  # 新闻标题
    translated_title = Column(TEXT, nullable=False)  # 翻译后的新闻标题
    time = Column(DateTime, nullable=False)  # 发布时间
    content = Column(TEXT, nullable=False)  # 新闻内容
    translated_content = Column(TEXT, nullable=False)  # 翻译后的新闻内容
    period_sign = Column(TEXT, nullable=False)  # 时期标志

    def __repr__(self):
        return f"<News {self.id} {self.site}>"


class Event(db.Model):
    """
    重要事件
    """
    __tablename__ = 'event'
    __table_args__ = {'extend_existing': True}

    id = Column(INTEGER, primary_key=True)  # 事件id，主键
    title = Column(TEXT, nullable=False)  # 事件标题
    translated_title = Column(TEXT, nullable=False)  # 翻译后的事件标题
    date = Column(DateTime, nullable=False)  # 举办时间
    institution = Column(TEXT, nullable=False)  # 举办机构
    link = Column(TEXT, nullable=False)  # 链接

    def __repr__(self):
        return f"<Event {self.id} {self.site}>"


if __name__ == '__main__':
    # db.create_all()
    u = User()
    u.password = '1'
    u.role_id = 0
    u.username = super
    print(u.password_hash)
