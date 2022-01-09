from lxml import etree
import datetime
import pymysql
import time


class gov_c:
    """
    author:于达海
    """

    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None

        xpath = r"//*[@id='js-results']/div/ul/li[*]/a/@href"
        root = etree.HTML(html).xpath(xpath)
        return ['https://www.gov.uk' + i for i in root]

    @staticmethod
    def title(html):
        xpath = r"//*[@class='gem-c-title__text govuk-heading-l' or @id='manual-title' or @class='gem-c-title__text govuk-heading-xl'] //text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return root[-1].strip()

    @staticmethod
    def maintext(html):
        xpath = r"//*[@id='content']//text()"
        root = etree.HTML(html).xpath(xpath)
        return "".join(root)

    @staticmethod
    def institution(html):
        xpath = "//*[@class='gem-c-metadata__definition']/*[@class='govuk-link']/text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return root[0].strip()

    @staticmethod
    def gettime(html):
        xpath = "//*[@class='gem-c-metadata__definition']/text()"
        root = etree.HTML(html).xpath(xpath)
        res = ""
        for i in root[::-1]:
            temp = i.replace("—", "").strip()
            if len(temp) > 3:
                t = time.strptime(temp, "%d %B %Y")
                res = time.strftime("%Y-%m-%d", t)
                break
        return res

    @staticmethod
    def abstract(html):
        xpath = "//*[@class='gem-c-lead-paragraph']/text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return root[0].strip()


class energy_c:
    """
    author:常奥飞
    """

    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None
        xpath = '//*[@id="block-particle-content"]/div/div/ul/*/div[3]/a/text()'
        root = etree.HTML(html).xpath(xpath)
        res = []
        for i in root:
            if isinstance(i, str):
                res.append(i)
            else:
                res.append(i.text)
        return res

    @staticmethod
    def title(html):
        xpath = r'//*[@id="block-pagetitle"]/div/div/div/h1/text()'
        root = etree.HTML(html).xpath(xpath)
        # print(root, 'eerr')
        if len(root) == 0:
            return ""

        return root[0].strip()

    @staticmethod
    def maintext(html):
        xpath = r'/html/body/div[2]/div/div/div/main/section/div/div//p/text()'
        root = etree.HTML(html).xpath(xpath)
        res = ''.join(root)
        return res

    @staticmethod
    def institution(html):
        xpath = '//*[@id="__layout"]/div/main/div/div[5]/div/div/div'
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return root[0].text.strip()

    @staticmethod
    def convert_date(s):
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']

        if s == None:
            return ''
        m, o = '', ''
        s1 = s.split(' ')
        # print(s1)
        mon, oth = s1[0], s1[1]
        for i in range(12):
            if mon in months[i]:
                m = i + 1
        s2 = oth.split(',')
        # print(s2)
        day, year = s2[0], s1[2]
        date = f'{year}-{m}-{day}'
        # try:
        # res = datetime.datetime.strptime(date,'%m-%d-%Y')
        res = date
        # except:
        #     return 0
        # print(type(res))
        return res, int(year)

    @staticmethod
    def gettime(html):
        xpath = '//*[@id="block-pagetitle"]/div/div/div/div[2]'
        root = etree.HTML(html).xpath(xpath)
        try:
            res = root[0].text
            res, year = energy_c.convert_date(res)
            # print(res)
            return res
        except:
            return ''

    @staticmethod
    def getyear(html):
        xpath = '//*[@id="block-pagetitle"]/div/div/div/div[2]'
        root = etree.HTML(html).xpath(xpath)
        try:
            res = root[0].text
            res, year = energy_c.convert_date(res)
            # print(res)
            return year
        except:
            return 0

    @staticmethod
    def abstract(html):
        xpath = '//*[@id="__layout"]/div/main/div/div[4]/div/p'
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return "null"
        return root[0].text.strip()


class mckinsey_c:
    """
    author:wdk
    """

    @staticmethod
    def title(html):
        if type(html) != str:
            return ""
        xpath = r"//*[@id='skipToMain']/main/section[1]/div/div/div/h1/text()|//*[@id='skipToMain']/main/section[1]/div/header/h3/text()|//*[@id='blogEntry']/div[1]/header/h1/text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return root[-1].strip()

    @staticmethod
    def maintext(html):
        if type(html) != str:
            return ""
        xpath = "//*[@id='divArticleBody']/article/*/text()|//*[@id='divArticleBody']/article/*/em/text()|//*[@id='divArticleBody']/article/ul/li/text()|//*[@id='blogEntry']/div[2]/div/article/div/p/text()"
        root = etree.HTML(html).xpath(xpath)
        return "".join(root)

    @staticmethod
    def gettime(html):
        if type(html) != str:
            return ""
        xpath = "//*[@id='skipToMain']/main/section[1]/div/div/div/footer/time/text()|//*[@id='skipToMain']/main/section[1]/div/header/div[2]/ul/li[1]/text()|//*[@id='blogEntry']/div[2]/div/article/div/p[1]/time/text()"
        root = etree.HTML(html).xpath(xpath)
        if root != []:
            temp = root[-1].replace(',', '')
            try:
                t = time.strptime(temp, "%B %d %Y")
                res = time.strftime("%Y-%m-%d", t)
                return res
            except:
                return ""
        else:
            return ""


class rand_c:
    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None
        # xpath = r"//*[@id='js-results']/div/ul/li[*]/a/@href"
        ### cago
        # xpath = "//*[@class='mb-3 heading search-result__title']/@href"
        ### rand.org
        xpath = "//*[@class='teasers list organic']//*[@class='url']//@href"

        root = etree.HTML(html).xpath(xpath)
        # print("root:", root)

        ### rand.org
        return [i for i in root]

    ### url中的主要字段：/events/, /topics/, /pubs/, /about/, /well-being/, /blog/
    @staticmethod
    def title(html):
        # xpath = r"//*[@class='gem-c-title__text govuk-heading-l' or @class='gem-c-heading govuk-heading-m govuk-!-margin-bottom-4']//text()"
        ### cago
        # xpath = "//*[@class='hero-impact zone-overlay']//*[@class='schema:name']//text()"
        ### rand.org
        xpath = "//h1/text()"
        root = etree.HTML(html).xpath(xpath)

        if len(root) == 0:
            return ""

        title_string = root[-1].strip()
        if "'" in title_string:
            title_string = title_string.replace("'", "\'")
        return title_string

    @staticmethod
    def maintext(html):
        # xpath = r"//*[@id='content']//p//text()|//*[@id='content']//h2//text()|//*[@id='content']//li//text()"
        ### cago
        # xpath = "//*[@class='body-text fs-lg' or 'heading heading--long-form js-long-form-nav-section']//text()"
        ### rand.org
        xpath = "//main[@id='page-content']//text()"

        root = etree.HTML(html).xpath(xpath)
        return "".join(root)


class belfercenter_c:
    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None
        xpath = r"//*[starts-with(@id, 'node-')]/div[2]/h2/a/@href"
        root = etree.HTML(html).xpath(xpath)
        res = []
        for i in range(len(root)):
            if isinstance(root[i], str):
                res.append("https://www.belfercenter.org/" + root[i])
            else:
                res.append("https://www.belfercenter.org/" + root[i].text)
        return res

    @staticmethod
    def title(html):
        xpath = r"//*[starts-with(@id, 'node-')]//h1/span/text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        # print(root)
        return root[-1].strip()

    @staticmethod
    def maintext(html):
        xpath = r"//*[starts-with(@id,'field-page-content')]//div//div/div//p/text()"
        root = etree.HTML(html).xpath(xpath)
        return "".join(root)

    @staticmethod
    def clean_date_str(s):
        s = s.strip('.')
        s = s.strip(',')
        return s

    @staticmethod
    def bel_data(timelist):
        months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                  'July': '07',
                  'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}

        # print(timelist)
        res = ''
        res += belfercenter_c.clean_date_str(timelist[2])
        res += '-'
        for j in months:
            if belfercenter_c.clean_date_str(timelist[0]) in j:
                res += months[j]
                break
        res += '-'
        res += belfercenter_c.clean_date_str(timelist[1])
        return res

    @staticmethod
    def gettime(html):
        try:
            xpath = './/span[contains(@class,"pub-date")]/text()[2]'
            root = etree.HTML(html).xpath(xpath)
        except(RuntimeError, AttributeError):
            root = []
        finally:
            if len(root) == 0:
                return ""
            else:
                if len(root[0].strip().split()) == 3:
                    return belfercenter_c.bel_data(root[0].strip().split())
                else:
                    return ""


class armedservices_c:
    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None
        xpath = r"//*[starts-with(@id,'group_e2cf2166')]/div/div/div/ol//li/h4/a/@href"
        root = etree.HTML(html).xpath(xpath)
        res = []
        for i in range(len(root)):
            if isinstance(root[i], str):
                res.append('https://armedservices.house.gov/' + root[i])
            else:
                res.append('https://armedservices.house.gov/' + root[i].text)
        return res

    @staticmethod
    def title(html):
        xpath = r"//*[starts-with(@id,'post_')]/div[1]/h1/a/text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return root[-1].strip()

    @staticmethod
    def maintext(html):
        xpath = r"//div[@class='post-content']/p/span/span/text()"
        root = etree.HTML(html).xpath(xpath)
        return "".join(root)

    @staticmethod
    def gettime(html):
        months = {'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
                  'July': '07',
                  'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12'}

        i = ''
        bol = 0
        try:
            mon_xpath = r".//span[contains(@class,'month')]/text()"
            mon_root = etree.HTML(html).xpath(mon_xpath)
            mon = mon_root[0].strip()
            day_xpath = r".//span[contains(@class,'day')]/text()"
            day_root = etree.HTML(html).xpath(day_xpath)
            day = day_root[0].strip()
            year_xpath = r".//span[contains(@class,'year')]/text()"
            year_root = etree.HTML(html).xpath(year_xpath)
            year = year_root[0].strip()
            i = year + '-' + months[mon] + '-' + day
            bol = 1
        except(RuntimeError, IndexError):
            i = ''
        finally:
            if bol == 1:
                return i
            else:
                return ''

    @staticmethod
    def abstract(html):
        try:
            xpath = "//*[@class='subtitle']//text()"
            root = etree.HTML(html).xpath(xpath)
        except(ValueError, RuntimeError, IndexError, None):
            root = []
        finally:
            if len(root) == 0:
                return ""
            return root[0].strip()


class defense_c:
    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None

        xpath = r"//*[starts-with(@id,'result-')]/span[1]/text()"
        # print(html)
        # print(type(html))
        root = etree.HTML(html).xpath(xpath)
        # 根据时间筛选
        # time_xpath = "/html/body/div[2]/div[2]/div/div[1]/div/div/div[2]/ul[2]//li/div[1]/text()"
        # time_root = etree.HTML(html).xpath(time_xpath)
        res = []
        for i in range(len(root)):
            # if choose_time(time_root[i].strip()) != None:
            if isinstance(root[i], str):
                res.append(root[i])
            else:
                res.append(root[i].text)
            # else:
            #     pass
        # print(res)
        return res

    @staticmethod
    def title(html):
        try:
            xpath = r"//*[starts-with(@id,'dnn_ctr')]/div/header/h1/text()"
            root = etree.HTML(html).xpath(xpath)
        # print(root)
        except(ValueError, RuntimeError, IndexError, None):
            xpath = r"//*[starts-with(@id,'dnn_ctr')]/div/div/div/div[1]/h1/text()"
            root = etree.HTML(html).xpath(xpath)
        finally:
            if len(root) == 0:
                return ""
            # print(root[-1].strip())
            return root[-1].strip()

    @staticmethod
    def maintext(html):
        try:
            xpath = r"//*[starts-with(@id,'dnn_ctr')]/div/div[2]//div/div[2]//p/text()"
            root = etree.HTML(html).xpath(xpath)
        except(ValueError, RuntimeError, IndexError, None):
            xpath = r"//*[starts-with(@id,'dnn_ctr')]/div/div/div/div[3]//p/text()"
            root = etree.HTML(html).xpath(xpath)
        finally:
            # print('maintext', root)
            return "".join(root)

    @staticmethod
    def institution(html):
        try:
            xpath = "//*[starts-with(@id,'node-')]/p/span[2]/text()"
            root = etree.HTML(html).xpath(xpath)
        except(ValueError, RuntimeError, None):
            root = []
        finally:
            if len(root) == 0:
                return ""
            ins = root[0].strip()
            ins = ins.strip('\n')
            # print(ins)
            return ins

    @staticmethod
    def gettime(html):
        try:
            xpath = './/span[contains(@class,"date")]/text()'
            root = etree.HTML(html).xpath(xpath)
        except(ValueError, RuntimeError, IndexError, UnboundLocalError):
            xpath = './/div[contains(@class,"date")]/text()'
            root = etree.HTML(html).xpath(xpath)
        finally:
            if len(root) > 0:
                # print(root[0].strip())
                ftime = belfercenter_c.bel_data(root[0].strip().split())
                # print(ftime)
                return ftime
            else:
                return ''

    @staticmethod
    def abstract(html):
        try:
            xpath = "//*[starts-with(@id,'dnn_ctr')]/div/div[2]/div[2]/div[2]/div[1]/text()"
            root = etree.HTML(html).xpath(xpath)
        except(ValueError, RuntimeError, IndexError, None):
            root = []
        finally:
            if len(root) == 0:
                return "null"
            # print(root[0].strip())
            return root[0].strip()

    @staticmethod
    def abs_list(alist):
        blist = []
        k = ''
        for i in alist:
            if i.startswith('\n'):
                k = k + i
            elif (i.startswith('\n') == False) and (i.endswith('\n') == False):
                k = k + i
            elif i.endswith('\n'):
                k = k + i
                blist.append(k)
                k = ''
        return blist


class whitehouse_c:
    @staticmethod
    def get_this_page_url(html):
        if html is None:
            return None
        xpath = r"//*[@class='col-md-10 col-lg-6']/article/header/h2/a/@href"
        root = etree.HTML(html).xpath(xpath)
        res = [str(i) for i in root]
        return res

    @staticmethod
    def title(html):
        xpath = r"//*[@id='content']/article/header/div/div/div/h1/text()"
        root = etree.HTML(html).xpath(xpath)
        if len(root) == 0:
            return ""
        return "".join(root)

    @staticmethod
    def maintext(html):
        xpath = r"//*[@id='content']/article/section/div/div//text()"
        root = etree.HTML(html).xpath(xpath)

        return "\n".join(root)

    @staticmethod
    def gettime(html):
        xpath = '//*[@id="content"]/article/header/div/div/div/div/time/text()'
        root = etree.HTML(html).xpath(xpath)
        if len(root)==0:
            return ""
        t = time.strptime(root[0], "%B %d, %Y")
        res = time.strftime("%Y-%m-%d", t)
        return res


if __name__ == '__main__':
    pass
    """
    db = pymysql.connect(host="10.1.38.243", user="root", password="123456", database="spider", port=3306)
    cur = db.cursor()
    submit_url(db, cur, "ydh", 2, "baidu.com", "2021-12-3", "fawda", "i am a sb", 1)
    submit_file(db, cur, "ydh", 2, "i am a sb")
    cur.close()
    db.close()
    """
