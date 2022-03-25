from aiospider.module.task import *
from multiprocessing import Process


class spider_main:
    def __init__(self, file_path="file"):
        self.file_path = file_path
    def gov_main(self, flag):
        if flag:
            gov(globe.db, globe.red, self.file_path)()

    def energy_main(self, flag):
        if flag:
            energy(globe.db, globe.red, self.file_path)()

    def mckinsey_main(self, flag):
        if flag:
            mckinsey(globe.db, globe.red, self.file_path)()

    def rand_main(self, flag):
        if flag:
            rand(globe.db, globe.red, self.file_path)()

    def belfercenter_main(self, flag):
        if flag:
            belfercenter(globe.db, globe.red, self.file_path)()

    def armedservices_main(self, flag):
        if flag:
            armedservices(globe.db, globe.red, self.file_path)()

    def defense_main(self, flag):
        if flag:
            defense(globe.db, globe.red, self.file_path)()

    def whitehouse_main(self, flag):
        if flag:
            whitehouse(globe.db, globe.red, self.file_path)()

    def __call__(self, name="all"):
        start_t = time.time()
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        utils.load_database_to_redis(globe.db, globe.red)

        # spider
        if name == "all":
            p1 = Process(target=self.gov_main, args=(1,))
            p2 = Process(target=self.energy_main, args=(1,))
            p3 = Process(target=self.mckinsey_main, args=(1,))
            p4 = Process(target=self.rand_main, args=(1,))
            p5 = Process(target=self.belfercenter_main, args=(1,))
            p6 = Process(target=self.armedservices_main, args=(1,))
            p7 = Process(target=self.defense_main, args=(1,))
            p8 = Process(target=self.whitehouse_main, args=(1,))
            multi = [p1, p2, p3, p4, p5, p6, p7, p8]
            [p.start() for p in multi]
            [p.join() for p in multi]
        else:
            eval("self.%s_main(1)" % name)
            # eval(name + "_main(1)")

        # summarization
        # upgrade_abs(globe.db)()
        # score
        # submit_Score(globe.db)()

        print("开始时间:%s" % start_time)
        print("结束时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        print("总用时:%.2f" % (time.time() - start_t))

    # def spider_run(name="all"):
    #     start_t = time.time()
    #     start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    #     utils.load_database_to_redis(globe.db, globe.red)
    #
    #     # spider
    #     if name == "all":
    #         p1 = Process(target=spider_main.gov_main, args=(1,self.file_path))
    #         p2 = Process(target=spider_main.energy_main, args=(1,self.file_path))
    #         p3 = Process(target=spider_main.mckinsey_main, args=(1,self.file_path))
    #         p4 = Process(target=spider_main.rand_main, args=(1,self.file_path))
    #         p5 = Process(target=spider_main.belfercenter_main, args=(1,self.file_path))
    #         p6 = Process(target=spider_main.armedservices_main, args=(1,self.file_path))
    #         p7 = Process(target=spider_main.defense_main, args=(1,self.file_path))
    #         p8 = Process(target=spider_main.whitehouse_main, args=(1,self.file_path))
    #         multi = [p1, p2, p3, p4, p5, p6, p7, p8]
    #         [p.start() for p in multi]
    #         [p.join() for p in multi]
    #     else:
    #         eval("spider_main.%s_main(1)" % name)
    #         # eval(name + "_main(1)")
    #
    #     # summarization
    #     # upgrade_abs(globe.db)()
    #     # score
    #     # submit_Score(globe.db)()
    #
    #     print("开始时间:%s" % start_time)
    #     print("结束时间:%s" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    #     print("总用时:%.2f" % (time.time() - start_t))


if __name__ == '__main__':
    spider_main()("gov")
    # spider_run()
