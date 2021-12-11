<h1 style="text-align: center">颠覆性技术系统</h1>

## TODO

### 1 App

- [x] 筛选（P0）
- [x] 用户管理（P1）
- [ ] 审核管理（P1）
- [x] 把数据从ali服务器迁移到tx3服务器，以后ali做开发机，tx3做生产环境（P2）
- [x] 机翻（P2）
- [x] PDF接口（P2）
- [x] 机构改成单个值
- [ ] 检索高亮策略还需调整

### 2 Spider

#### 2.0 爬虫内容
- [x] 控制内容精确程度，尽量使用高级检索

#### 2.1 多线程爬虫

- [ ] 实现多线程

#### 2.2 爬虫管理/调度器

- [ ] 主要实现

#### 2.3 下载

- [x] 下载数据流程化（PDF、HTML）
- [x] 确认下载文件夹、文件名有没有放错

#### 2.4 数据导入
- [x] 英泽学长的美国数据统一导入

### 3 Process

#### 3.0 文件管理
最核心的资源是文件，所以其实最核心的地方在于文件管理系统，
刚才整理文件特别心烦，突然意识到这个问题。梳理一下，文件系统主要应该具有这些功能：

#### 3.1 Modify

数据库和文件整理

#### 3.2 Field
- [x] 领域分类器
  - 做了一个领域特定的词表
  - 如何体现特征指向性



#### 3.3 Translate

翻译标题和正文

#### 3.4 Parse

解析PDF和HTML

### 4 整体架构

通用工具的编写

#### 4.1 测试环境
- [ ] 如何快速构建同步的测试环境数据库



# 边开发边学习

## 踩到的坑

- Flaks login 有个坑，在head里面要引用current user的话，需要在import的时候加上 with context
- with open 一个文件，如果用的是'w'模式，那么会创建，哪怕没有任何write行为
- app.app_context().push()，如果外部无法使用flask-sqlalchemy，在 import app 之后加上这一句

## 事故记录
20210530 数据库覆盖事故（field字段都损失掉了）

1. 上线前一定要看到测试数据库的运行结果
2. 爬虫一定要做缓存
3. 一定要定时做数据库备份

## 几个爬虫小知识

> 基本都来自《用python写网络爬虫》

### urllib

`urllib`名副其实，是关于url的工具包，在有一些实用的功能：

##### 解析链接：urlparse

用来分析链接，可以获取域名、参数等

```python
from urllib.parse import urlparse
result = urlparse('http://www.bigdata17.com')
print(result)
# ParseResult(scheme='http', netloc='www.bigdata17.com', path='', params='', query='', fragment='')
```

##### 拼接链接：urljoin

用来合并相对链接

```python
import urllib.parse as urlparse
urlparse.urljoin('http://www.cwi.nl/%7Eguido/Python.html', '//www.python.org/%7Eguido')
# 'http://www.python.org/%7Eguido'
```

##### 解析robots.txt：urllib.robotparser

可以解析网站根目录下的`robots.txt`对爬虫进行一些指引（比如爬虫间隔），虽然我觉得实际上没什么用，要求10秒我就5秒也没封IP。

### requests_cache

### redis task

### multitask

- [increment](https://www.zhihu.com/question/19793879)

## 打日志
```python
import logging
logging.basicConfig(format='%(asctime)s | %(levelname)s | %(filename)s | %(funcName)s | %(message)s', level=logging.INFO, datefmt='%m-%d %H:%M:%S')
```

添加 filter
```python
import logging
class SupMinerFilter(logging.Filter):
    def filter(self, record):
        return not record.funcName == 'handle_undefined_char'
logging.root.filters.append(SupMinerFilter())
```


<div STYLE="page-break-after: always;"></div>

# 领域分类阶段性结果

> 这里说说领域分类器的具体技术实现

## 1.方法一（向量）

### 1.1 原理（余弦相似度）

词向量法为目前使用的方法

- 优点是能够灵活控制词表，通过vector计算领域主题的相似性
- 缺点是只通过词分布来计算领域略显单薄

1. 文章：根据 Title 和 Abstract 的`词频`生成 WordBag 向量
   - 注意整个基底是以领域词表为准的，很多文章中的词并不出现
   - 注意其中有大量的freq都是0，因为文章词数远小于领域的词数，一般freq主要在0～5之间

$$
\mathbf{V_{article\_in\_field}} = [freq\_word_1, freq\_word_2, ... , freq\_word_n]
$$

2. 领域：每一个领域生成一个综合考虑`词频`和`总词数`的向量
   - 每一个词权重的计算方法为：$weight\_word_n = freq\_word_1 \div \Sigma^{n}_{i=1}freq\_word_i$
     - 之所以除以总词数，因为要确保不同领域对同一个文章的相似度是归一化的

$$
\mathbf{V_{field}} = [weight\_word_1, weight\_word_2,..., weight\_word_n]
$$

3. 两者的结合方式如下
   - 公式中使用模长作为归一化的工具
   - 余弦相似度最本质的特点就是两个向量方向一致的时候，相似度最高

$$
similarity = \dfrac{\mathbf{V_{article\_in\_field}} \cdot \mathbf{V_{field}}}
{|\mathbf{V_{article\_in\_field}}| \cdot |\mathbf{V_{field}}|}
$$

### 1.2 如何调整效果

#### 1.2.1 附加词表

初步决定按照分类的级别给附加词表进行向量赋权值，具体怎么加权重是值得商榷的，因此下面我对这个权重应该取多少进行了一定的探索：

- 首先看最基础的事情：分布情况或者说是长尾情况；
- 然后再看主题词袋中权重排名靠前的代表性词汇；

##### 先看看原始词表的长尾情况

下面首先查看每一个field的词频分布，下图==横纵坐标全部统一==，其中==纵坐标截断比较多==，但是0～10长什么样很容易推测。==标题里==说明了每个领域词袋的==词数量（去重）和词频总和==，结论如下：

- 不同领域词频很不均匀，`Artificial Intelligence`和`gene technology`明显特别多
- 我发现词太少（因为这本身说明该主题文章就少）才是真正的问题（之前觉得词太多是问题），因为词少了对领域的刻画就不准确了，就很容易出现“常用词”，比如最典型的，`Modern Transportation Technology`和`new generation of information technology`，他们的词恰恰是最少的，特别是在我删了低频词的基础上（必须删，不然根本==跑不动==，当然像transportation和information可以考虑不删，但是他们确实是少）

![image-20210720160238689](http://pic.fishiu.com/uPic/h4mEit.png)

##### 重要主题词情况

为了更好了解每个领域重要词的大致的分布，我们查看每一个领域的词权重的==前十名==：

- ==注意==：这里删掉了词频 <10 的词（我觉得这里我失误了，之前贪图跑得快），虽然这些词很多，但是用词向量的话影响不大

```
Artificial Intelligence 该领域的词数为： 2711
[0.1361 0.0354 0.0211 0.0194 0.0168 0.0095 0.0089 0.0067 0.0064 0.006 ]

**** Biotechnology 该领域的词数为： 850
[0.1284 0.0088 0.0071 0.0067 0.0059 0.0058 0.0055 0.005  0.0047 0.0046]

**** Intelligent manufacturing 该领域的词数为： 249
[0.0464 0.0283 0.0259 0.0204 0.0203 0.0183 0.0172 0.0163 0.0155 0.0133]

Modern Transportation Technology 该领域的词数为： 18
[0.1183 0.1095 0.0888 0.0799 0.0651 0.0621 0.0533 0.0444 0.0444 0.0444]

aerospace technology 该领域的词数为： 205
[0.0494 0.0494 0.0267 0.0251 0.0245 0.0241 0.0154 0.015  0.0138 0.0123]

big data technology 该领域的词数为： 855
[0.1496 0.0258 0.0224 0.022  0.0158 0.0156 0.0135 0.0117 0.0115 0.0099]

gene technology 该领域的词数为： 3109
[0.0151 0.0117 0.0109 0.0085 0.0078 0.0076 0.0066 0.0062 0.0062 0.0059]

marine technology 该领域的词数为： 656
[0.0158 0.0134 0.0099 0.0096 0.0091 0.0086 0.0081 0.0081 0.0074 0.0071]

new generation of information technology 该领域的词数为： 194
[0.0283 0.022  0.0207 0.0207 0.0188 0.0188 0.0184 0.0177 0.0171 0.0167]

**** new material technology 该领域的词数为： 2375
[0.0098 0.0085 0.0074 0.006  0.0051 0.005  0.0048 0.0047 0.0047 0.0045]
```

可以有以下几点结论：

- 删小词频 <10 太狠了，要控制的小一点（之后看一下短尾情况）
- 有的领域几乎没有代表性词汇（主要是因为词太多）
  - Intelligent manufacturing
  - aerospace technology
  - gene technology
  - new material technology

##### 这是一个结合了分类结果和主题词袋规模的图

一定程度上证实了我的想法：分类太容易是因为词太少了

![image-20210720171833066](http://pic.fishiu.com/uPic/ZqcKUz.png)

##### 这里贴一张横坐标0～20的局部图

![image-20210720165457085](http://pic.fishiu.com/uPic/beuQsd.png)

#### 1.2.2 删除词

- 删除（新代信息技术等高频类中的）低频词
  - 这是化老师提出的，我觉得低频词其实影响很微弱的
  - 我觉得反而应该删除一些奇葩的高频词
- 使用 IDF 降低`通用词的权重`
  - 计算方法：每一个词在十个词表的总和中计算词频作为 IDF，然后在每一个领域中单独除以这个 IDF
  - 其实我觉得用 IDF 是有些奇怪的，因为如果故意降低 Weight，那么 IDF 会导致最终结果不准
- 综上，我觉得目前最好的办法是单独控制词频阈值



### 1.3 实验结果

首先确定阈值（尽可能让词袋分布比较均匀，但效果还是比较勉强）

```python
threshold = {
    'Artificial Intelligence': 9,
    'Biotechnology': 8,
    'Intelligent manufacturing': 20,
    'Modern Transportation Technology': 7,
    'aerospace technology': 20,
    'big data technology': 6,
    'gene technology': 70,
    'marine technology': 25,
    'new generation of information technology': 25,
    'new material technology': 70
}
```

重新run了一遍分类器，以0.1作为阈值，以0.15作为主次类别差值阈值（大于阈值则只要主类），对比结果如图。

```json
// 主类别
{"无类别": 3406, "人工智能技术": 0, "生物技术": 2, "智能制造": 0, "现代交通技术": 1793, "空天技术": 27, "大数据技术": 5, "基因技术": 8, "海洋技术": 171, "新代信息通信技术": 5169, "新材料技术": 0}

// 次类别
{"人工智能技术": 0, "生物技术": 0, "智能制造": 0, "现代交通技术": 36, "空天技术": 3, "大数据技术": 0, "基因技术": 0, "海洋技术": 361, "新代信息通信技术": 6, "新材料技术": 0}
```



![image-20210720230233104](http://pic.fishiu.com/uPic/slYqNk.png)

## 2. 方法二（深度分类模型）

因为任务本身很简单，最好的分类模型（比如Fasttext 或者 Bert）都能直接用

关键是标注数据，目前看上了[MAG数据库（链接）](https://academic.microsoft.com/topics)，他有非常丰富的类别标签，我感觉我们想要的他都能找到，但是MAG一共有`四层`标签，因此挑选哪些类别是一个问题。

<img src="http://pic.fishiu.com/uPic/B3V7TR.png" alt="image-20210720161708299" style="zoom:33%;" />

未完待续...（数据已有现成，主要工作是挑一下类别，以及后续的训练）



## 颠覆性技术领域分类审核工作

8月20日

### 目标

为更好呈现分类效果，顺便为未来有监督研究提供辅助，需要对目前入库1000条左右的数据进行领域分类的审核。

### 分类标签

十大具体领域：

- 人工智能技术
- 新代信息通信技术
- 大数据技术
- 新材料技术
- 现代交通技术
- 空天技术
- 生物技术
- 海洋技术
- 智能制造
- 基因技术

外加一个“综合”标签

### 分类规则

优先考虑标题（因为快速）大意判断即可，没看懂的则进一步：标题->摘要->关键词->正文等内容进行判断，**尽量每篇控制在30秒**之内，不用太纠结。

拿不准的、很含糊的就分到“综合”即可，有其他问题的可以记录一下文章ID后续在群里汇报。

> 几点说明
>
> - 由于这10大类别本身不互斥、不完整（也就是不太科学），因此我们做一些约束
> - 首先优先考虑是否属于某个**“具体领域”**：交通、材料、空天、生物、海洋、基因
> - 如果不属于上面具体领域，那么考虑是否属于**大数据、智能制造**
> - 还未分类则考虑**人工智能、新代信息通信技术**
> - 最终仍无处可去则分入**”综合类“**

### 网站使用流程

首先登陆http://152.136.104.78:5000，账号已经帮大家注册，**用户名**为姓名缩写（如：jxy），**密码**为1

登陆后即首页，首页底部有页面跳转按钮，也可以直接在地址栏**改page参数**进行跳转，如：http://152.136.104.78:5000/index.html?page=53 回车后则跳到53页，点击标题就会跳转到如下的政策详细信息界面：

![image-20210815143739954](http://pic.fishiu.com/uPic/tdVEKw.png)

下图是审核界面说明，注意**地址栏中的ID**就是该文章的ID，有问题请记下此ID

![image-20210815143301452](http://pic.fishiu.com/uPic/lK28qo.png)

### 分工

注意在主页选择页码时**不要点击任何筛选或者是排序**，一共有101页，分工如下

| 负责人 | 页数               |
| ------ | ------------------ |
| 于达海 | 1~10, 51~60        |
| 王宏光 | 11~20, 61~70       |
| 常奥飞 | 21~30, 71~80       |
| 张家烁 | 31~40, 81~90       |
| 宋嘉骐 | 41~50, 91~100      |
| 陈科锜 | 近期后续新入库数据 |
| 金笑缘 | 近期后续新入库数据 |

