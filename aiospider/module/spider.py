import random
import time
import aiohttp
import asyncio
from fake_useragent import UserAgent
from aiospider.module.rediscache import RedisCache


class downloader:
    def __init__(self, url_list, header=True, delay=0, proxies=None, cache=dict(),
                 timeout=60,
                 num_retries=10):
        # 0 random.uniform(0,0.5) random.random()
        self.urls = url_list
        self.header = header
        self.delay = delay
        self.proxies = proxies
        self.cache = cache
        self.timeout = timeout
        self.num_retries = num_retries

        self.result = [None] * len(self.urls)
        self.fail = []

    async def download(self, id, url, retries):

        # time.sleep(self.delay)
        await asyncio.sleep(random.uniform(0, 0.5))
        try:
            cache_result = self.cache[url]
            # if cache_result != "a":
            #     self.result[id] = cache_result
        except (KeyError, TypeError):
            cache_result = None

        html = None
        while html is None and cache_result is None and retries:
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = None
            if self.header:
                headers = {'User-Agent': UserAgent().random}
            #print(headers)
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers=headers, proxy=proxy, timeout=self.timeout) as res:
                        html = await res.text()
                        if res.status >= 400:
                            print('wrong %s' % res.status)
                            # time.sleep(5)
                            await asyncio.sleep(5)
                            html = None
                        # result = await self.parser(html)
                        else:
                            self.result[id] = html
                            if self.cache:
                                # self.cache[url] = html
                                self.cache[url] = "a"
            except:
                # time.sleep(5)
                await asyncio.sleep(5)
                print('connect error')
                html = None
                # self.result[id] = await self.download(id, url, retries - 1)

            retries -= 1
            if retries == 0:
                print("one fail")
                self.result[id] = html
                self.fail.append(url)

    def main(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task_list = [asyncio.ensure_future(self.download(i[0], i[1].strip(), self.num_retries)) for i in
                     enumerate(self.urls)]
        task_gather = asyncio.gather(*task_list)
        loop.run_until_complete(task_gather)
        return self.result

    def __call__(self):
        return self.main()


class download:
    def __init__(self, url_list, header=True, callback=lambda x: x, cache=None):
        self.url_list = url_list
        self.callback = callback
        self.cache = cache
        self.header = header

    def __call__(self):
        result_list = []
        html_list = downloader(self.url_list, cache=self.cache,header=self.header)()

        for html in html_list:
            result_list.append(self.callback(html))

        return result_list


if __name__ == '__main__':
    url = ["https://www.whitehouse.gov/?paged=1&s=technology"]
    html_list = download(url,header=False)()
    print(html_list)
