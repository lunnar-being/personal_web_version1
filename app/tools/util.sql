-- todo 这里的密码记得改/删掉
ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'A14.55d2%Lw2';


-- 英文标题索引
ALTER TABLE policy_text
    ADD FULLTEXT INDEX policy_title_index (original_title) WITH PARSER ngram;
-- 检索举例
SELECT id, original_title, COUNT(1)
FROM policy_text
WHERE MATCH(policy_text.original_title) AGAINST('medical technology' IN NATURAL LANGUAGE MODE)
LIMIT 10;


-- 中文标题检索
ALTER TABLE policy_text
    ADD FULLTEXT INDEX policy_trans_title_index (translated_title) WITH PARSER ngram;
-- 删除索引
DROP INDEX policy_trans_title_index
    ON policy_text;
-- 检索举例
SELECT id, original_title, translated_title
FROM policy_text
WHERE MATCH(policy_text.translated_title) AGAINST('纳米' IN NATURAL LANGUAGE MODE)
LIMIT 10;

-- 中文摘要检索
ALTER TABLE policy_text
    ADD FULLTEXT INDEX policy_trans_abs_index (translated_abstract) WITH PARSER ngram;

-- 中文摘要检索
ALTER TABLE policy_text
    ADD FULLTEXT INDEX policy_trans_keyword_index (translated_keywords) WITH PARSER ngram;

-- 英文关键词索引
ALTER TABLE policy_text
    ADD FULLTEXT INDEX policy_keywords_index (keywords) WITH PARSER ngram;


-- 查看翻译进度情况
SELECT *, COUNT(1)
FROM file
WHERE filetype = '3'
  AND savename IS NULL;
-- 标题翻译进度
SELECT COUNT(1)
FROM policy_text
WHERE translated_title IS NOT NULL;

-- 查看政策的format情况
SELECT site, COUNT(1)
FROM policy_text
WHERE format_file IS NOT NULL
GROUP BY site;
# WHERE policy_text.source_url IS NULL;


-- 3725条已知链接但是还没有存下来
SELECT COUNT(f.extension), f.extension
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
WHERE file_url IS NOT NULL
  AND f.savename IS NULL
GROUP BY f.extension;
-- list the not downloaded file
SELECT policy_text.file_url
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
WHERE file_url IS NOT NULL
  AND f.savename IS NULL;


-- 以下主要是用来检查文件缺失情况的
SELECT *
FROM policy_text
WHERE policy_text.original_file IS NULL;

SELECT *
FROM file
WHERE filetype = 1
  AND file.savename IS NULL;

-- 12997 12998
SELECT *
FROM policy_text
WHERE policy_text.original_file NOT IN (
    SELECT id
    FROM file
    WHERE filetype = 1
);


-- 有哪些是PDF格式的
SELECT *
FROM file
WHERE filetype = 1
  AND savename IS NOT NULL
  AND savename REGEXP '[^\.]pdf$';

UPDATE file
SET extension = LOWER(extension);

-- field distribution
SELECT COUNT(1) AS field_count, norm_field
FROM policy_text
WHERE norm_field IS NOT NULL
#   AND format_file IS NOT NULL
#   AND `RANK` IS NOT NULL
  AND id < 12000
GROUP BY norm_field
ORDER BY field_count DESC;

-- 增加来源一栏（有点冗余，但是有必要）
SELECT REGEXP_SUBSTR(source_url, '(?:https|http):\/\/([a-zA-Z\.]+)\/', 1, 1)
FROM policy_text
LIMIT 10;


-- 新增字段
-- 计算后的领域
ALTER TABLE policy_text
    ADD norm_field VARCHAR(100) NULL COMMENT '计算后的领域';
-- 站点域名
ALTER TABLE policy_text
    ADD site VARCHAR(100) NULL COMMENT '站点域名';


UPDATE policy_text
SET norm_field =(
    CASE
        WHEN (norm_field = 'Artificial Intelligence') THEN '人工智能技术'
        WHEN (norm_field = 'Biotechnology') THEN '生物技术'
        WHEN (norm_field = 'Intelligent manufacturing') THEN '智能制造'
        WHEN (norm_field = 'Modern Transportation Technology') THEN '现代交通技术'
        WHEN (norm_field = 'aerospace technology') THEN '空天技术'
        WHEN (norm_field = 'big data technology') THEN '大数据技术'
        WHEN (norm_field = 'gene technology') THEN '基因技术'
        WHEN (norm_field = 'marine technology') THEN '海洋技术'
        WHEN (norm_field = 'new generation of information technology') THEN '新代信息通信技术'
        WHEN (norm_field = 'new material technology') THEN '新材料技术'
        ELSE (norm_field)
        END);


-- 有多少没有站点信息
SELECT ISNULL(site) AS is_site_null, COUNT(1)
FROM policy_text
GROUP BY is_site_null;
-- 都是些什么
SELECT *
FROM policy_text
WHERE ISNULL(site);


-- 查看site分布
SELECT COUNT(1) AS site_cnt, site
FROM policy_text
GROUP BY site
ORDER BY site_cnt DESC;

-- 查看来源分布(已经下载文件的)
SELECT COUNT(1) AS site_cnt, site
FROM policy_text
WHERE format_file IS NOT NULL
GROUP BY site
ORDER BY site_cnt DESC;

-- 查看有多少rank 6924
SELECT COUNT(1)
FROM policy_text
WHERE `RANK` IS NOT NULL;

-- 查看有多少rank和norm_filed 6924 -> 5208
SELECT COUNT(1)
FROM policy_text
WHERE `RANK` IS NOT NULL
  AND norm_field IS NOT NULL;

-- 查看rank排前limit名的文章
SELECT original_title, norm_field, id, site, `RANK`
FROM policy_text
WHERE norm_field IS NOT NULL
ORDER BY `RANK` DESC
LIMIT 30;

-- 查看rank为0的文章
SELECT original_title, norm_field, policy_text.id, site, f.id, f.savename, `RANK`
FROM policy_text
         JOIN file f ON f.id = policy_text.format_file
WHERE `RANK` = 0;

-- ext and filetype distribution
SELECT COUNT(1) AS cnt, extension, filetype
FROM file
GROUP BY extension, filetype
ORDER BY cnt DESC;

-- 查看机构分布
SELECT COUNT(1) AS cnt, institution
FROM policy_text
GROUP BY institution
ORDER BY cnt DESC;

-- 查看nation分布 eu: 16344, uk: 6829, america: 3299
SELECT COUNT(1) AS cnt, nation
FROM policy_text
GROUP BY nation
ORDER BY cnt DESC;

-- 统一 nation
UPDATE policy_text
SET nation = '美国'
WHERE nation = 'america';
UPDATE policy_text
SET nation = '英国'
WHERE nation = 'UK';
UPDATE policy_text
SET nation = '欧盟'
WHERE nation = 'EU';

-- 统一语言
UPDATE policy_text
SET language = '英语'
WHERE language = 'English'
   OR language = 'EN';

-- 查看file_type分布 eu: 16344, uk: 6829, america: 3299
SELECT COUNT(1) AS cnt, f.filetype
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
GROUP BY f.filetype
ORDER BY cnt DESC;

-- 查看有多少是有savename的: 8758 -> 10110
SELECT policy_text.id, policy_text.source_url, f.savename
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
WHERE f.savename IS NOT NULL;

-- update site(domain)
UPDATE policy_text
SET policy_text.site = 'op.europa.eu'
WHERE source_url REGEXP 'https://op.europa.eu.*';
-- update site(domain)
UPDATE policy_text
SET policy_text.site = 'www.govinfo.gov'
WHERE source_url LIKE '*govinfo.gov*';

SELECT site, source_url
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
WHERE filetype = 1
  AND extension = 'html'
  AND savename IS NULL;

-- file distribution (valid)
SELECT site, COUNT(1)
FROM policy_text
WHERE `RANK` > 6.7
#   AND format_file IS NOT NULL
GROUP BY site;

-- 调整阈值
SELECT COUNT(1)
FROM policy_text
WHERE `RANK` > 6.7;

SELECT policy_text.id, original_title, savename, `RANK`
FROM policy_text
         JOIN file f ON f.id = policy_text.translated_file
WHERE `RANK` > 0
ORDER BY `RANK` DESC;

-- 初始化 fd state
UPDATE file
SET extra_info = JSON_OBJECT('fd_state', JSON_ARRAY())
WHERE filetype = 1
  AND extra_info IS NULL;


SELECT policy_text.id,
       f.id,
       policy_text.source_url,
       policy_text.file_url,
       policy_text.original_title,
       f.savename,
       f.update_time
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
WHERE f.savename = 'origin_b0bcdb4e1c35165c13aa4bf9b0554e04.pdf';

-- 查看policy的重复情况
SELECT COUNT(*) AS cnt, file_url, site
FROM policy_text
GROUP BY file_url
HAVING cnt > 1
ORDER BY cnt DESC;

-- 清楚wyz的savename
UPDATE file
SET savename = NULL
WHERE file.id IN (
    SELECT original_file
    FROM policy_text
    WHERE site = 'www.govinfo.gov'
)
  AND filetype = 1;

-- 查看有originfile但是没有formatfile的policy
SELECT policy_text.id AS policy_id, f.extra_info, f.extension, policy_text.site
FROM policy_text
         JOIN file f ON f.id = policy_text.original_file
WHERE policy_text.spider_condition = 299
  AND policy_text.format_file IS NULL;

-- 看看还有多少没有翻译
SELECT COUNT(1)
FROM policy_text
WHERE `RANK` > 6.7
  AND translated_file IS NULL;


-- 标题重复情况
SELECT original_title, COUNT(original_title) AS cnt
FROM policy_text
WHERE original_title IS NOT NULL
AND `rank` > 6.7
GROUP BY original_title
ORDER BY cnt DESC;

-- 机构及其数量
SELECT institution, COUNT(institution) AS cnt
FROM policy_text
WHERE institution IS NOT NULL
AND `rank` > 6.0
ORDER BY cnt DESC;

-- 机构去重后数量
SELECT COUNT(1)
FROM (
         SELECT institution
         FROM policy_text
         WHERE `rank` > 6.0
         GROUP BY institution
     ) AS ins;

UPDATE policy_text
SET recommend = 1
WHERE `rank` > 28;
