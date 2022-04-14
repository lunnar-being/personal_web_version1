from aiospider.module.callback import *
from aiospider.module.utils import *
from aiospider.module.entity import *
from aiospider.module.spider import *
import json


class gov:
    def __init__(self, db, cache=None, file_path="file", callback_class=gov_c):
        self.url_list = [
            "https://www.gov.uk/search/all?content_purpose_supergroup%5B%5D=guidance_and_regulation&keywords=science+and+technology&order=relevance&page=" + "%s" % i + "&public_timestamp%5Bfrom%5D=2020"
            for i in range(1, 3)]
        # 101
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class
        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("gov")
        for i in self.url_list:
            start = time.time()

            this_url = download([i], callback=self.callback_class.get_this_page_url)()
            this_url = [k for k in this_url[0] if k is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]
            institutions = [self.callback_class.institution(i) for i in htmls]
            abstracts = [self.callback_class.abstract(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]
                e["time"] = gettimes[j]
                e["institution"] = institutions[j]
                e["abstract"] = abstracts[j]
                e["source_url"] = this_url[j]

                mt = maintexts[j]

                if len(mt) > 50 and e["title"] != "null":
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)

            print("gov:%s %.2f" % (self.page, time.time() - start))
            self.page += 1

        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class energy:
    def __init__(self, db, cache=None, file_path="file", callback_class=energy_c):
        self.url_list = [f"https://www.energy.gov/search/site?keywords=science%20and%20technology&page={i}"
                         for i in range(1, 2)]
        # 2014
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class
        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("energy")
        for i in self.url_list:
            start = time.time()

            this_url = download([i], callback=self.callback_class.get_this_page_url)()
            this_url = [k for k in this_url[0] if k is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]
            getyears = [self.callback_class.getyear(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]
                e["time"] = gettimes[j]
                e["institution"] = "Department of Energy"
                e["source_url"] = this_url[j]
                mt = maintexts[j]
                if e["title"] != "null" and len(mt) > 50 and int(getyears[j]) >= 2020:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)

            print("energy:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class mckinsey:

    def __init__(self, db, cache=None, file_path="file", callback_class=mckinsey_c):
        self.url_list = [
            'https://mckapi.mckinsey.com/api/globalsearch?q=technology&start=%s&sort=date&pageFilter=insights' % i for i
            in range(1, 2)]
        # 426
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class

        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("mckinsey")
        for i in self.url_list:
            start = time.time()

            html_pre = download([i], cache=self.cache)()
            if html_pre[0] is None:
                continue
            html_json = json.loads(html_pre[0])["results"]

            this_url = [i["url"] for i in html_json if i["url"] is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)
            titles = [self.callback_class.title(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            for j in range(length):
                e = entity()
                e["source_url"] = this_url[j]

                e["title"] = titles[j]
                e["time"] = gettimes[j]

                mt = maintexts[j]

                if e["time"] != 0 and e["title"] != "null" and len(mt) > 50:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)
            print("mckinsey:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class rand:
    def __init__(self, db, cache=None, file_path="file", callback_class=rand_c):
        self.url_list = [
            "https://www.rand.org/search.html?query=science+technology&sortby=date&page=" + "%s" % i for i in
            range(1, 2)
        ]
        # 13
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class
        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("rand")
        for i in self.url_list:
            start = time.time()

            this_url = download([i], callback=self.callback_class.get_this_page_url)()
            this_url = [k for k in this_url[0] if k is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]

                e["source_url"] = this_url[j]

                mt = maintexts[j]
                if e["title"] != "null" and len(mt) > 50:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)
            print("rand:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class belfercenter:
    def __init__(self, db, cache=None, file_path="file", callback_class=belfercenter_c):
        self.url_list = [
            f"https://www.belfercenter.org/search/all?q=science%20and%20technology&from=01/01/2020&page={i}"
            for i in range(0, 2)]
        # 63
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class

        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("belfercenter")
        for i in self.url_list:
            start = time.time()

            this_url = download([i], callback=self.callback_class.get_this_page_url)()
            if len(this_url) == 0:
                continue
            this_url = [k for k in this_url[0] if k is not None]


            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]
                e["time"] = gettimes[j]
                e["source_url"] = this_url[j]

                mt = maintexts[j]
                if e["title"] != "null" and len(mt) > 50:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)
            print("belfercenter:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class armedservices:
    def __init__(self, db, cache=None, file_path="file", callback_class=armedservices_c):
        self.url_list = [f"https://armedservices.house.gov/search?q=science&page={i}" for i in
                         range(1, 2)]
        # 4
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class
        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("armedservices")
        for i in self.url_list:
            start = time.time()

            this_url = download([i], callback=self.callback_class.get_this_page_url)()
            this_url = [k for k in this_url[0] if k is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]
            abstracts = [self.callback_class.abstract(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]
                e["time"] = gettimes[j]
                e["source_url"] = this_url[j]
                e["abstract"] = abstracts[j]

                mt = maintexts[j]
                if e["title"] != "null" and len(mt) > 50:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)
            print("armedservices:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class defense:
    def __init__(self, db, cache=None, file_path="file", callback_class=defense_c):
        self.url_list = [
            f"https://search.usa.gov/search?affiliate=defensegov&page={i}&query=science&utf8=%26%23x2713%3B" for i in
            range(1, 2)]
        # 91
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class
        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("defense")
        for i in self.url_list:
            start = time.time()

            """
            xpath = "//*[starts-with(@id,'result-')]/span[2]/text()"
            flag = 0
            ab = download([i], cache=self.cache)()[0]
            if type(ab) == str:
                root = etree.HTML(ab).xpath(xpath)
                abstracts = self.callback_class.abs_list(root)
                flag = 1
            """
            this_url = download([i], callback=self.callback_class.get_this_page_url)()
            this_url = [k for k in this_url[0] if k is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]
            institutions = [self.callback_class.institution(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]
                e["time"] = gettimes[j]
                e["source_url"] = this_url[j]

                # if flag:
                #     e["abstract"] = abstracts[j]
                e["institution"] = institutions[j]

                mt = maintexts[j]
                if e["title"] != "null" and len(mt) > 50:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)
            print("defense:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


class whitehouse:
    def __init__(self, db, cache=None, file_path="file", callback_class=whitehouse_c):
        self.url_list = ["https://www.whitehouse.gov/?paged=%s&s=technology" % i for i in range(1, 2)]  # 63
        self.db = db
        self.cur = self.db.cursor()
        self.cache = cache
        self.callback_class = callback_class
        self.page = 1
        self.file_path=file_path

    def __call__(self):
        ec = entity_collect("whitehouse")
        for i in self.url_list:
            start = time.time()

            this_url = download([i], callback=self.callback_class.get_this_page_url, header=False)()
            this_url = [k for k in this_url[0] if k is not None]
            if len(this_url) == 0:
                continue

            htmls = download(this_url, cache=self.cache, header=False)()
            z = [i for i in zip(this_url, htmls) if i[1] != None]
            unzip = list(zip(*z))
            if unzip == []:
                continue
            this_url, htmls = unzip[0], unzip[1]
            length = len(htmls)

            titles = [self.callback_class.title(i) for i in htmls]
            maintexts = [self.callback_class.maintext(i) for i in htmls]
            gettimes = [self.callback_class.gettime(i) for i in htmls]

            for j in range(length):
                e = entity()
                e["title"] = titles[j]
                e["time"] = gettimes[j]
                e["source_url"] = this_url[j]
                e["institution"] = "White House"

                mt = maintexts[j]
                if e["title"] != "null" and len(mt) > 50:
                    ec["new_title"] = e["title"].replace("\"", "")
                    # utils.file_write(e["title"], mt,self.file_path)
                    # utils.submit(self.db, self.cur, e)
            print("whitehouse:%s %.2f" % (self.page, time.time() - start))
            self.page += 1
        utils.upgrade_collect(self.db, self.cur, ec)
        # self.cur.close()
        # self.db.close()


if __name__ == '__main__':
    # red = RedisCache()
    # db = pymysql.connect(host="81.70.102.186", user="root", password="YDH@henniu123", database="spider", port=3306)
    # utils.load_database_to_redis(db,red)
    # gov(db, red)()
    # energy(db, red)()
    # mckinsey(db, red)()
    # rand(db)()
    # belfercenter(db)()
    # armedservices(db)()
    # defense(db, cache=red)()
    # whitehouse(globe.db)()
    pass
