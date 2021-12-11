CREATE TABLE file
(
    id          int AUTO_INCREMENT
        PRIMARY KEY,
    filetype    tinyint                 NULL,
    name        text                    NULL,
    savename    text                    NULL,
    extension   char(5)                 NOT NULL,
    size        varchar(20) DEFAULT '0' NULL,
    create_time datetime                NULL,
    update_time datetime                NULL,
    download    int         DEFAULT 0   NULL
);



CREATE TABLE policy_text
(
    id               int AUTO_INCREMENT
        PRIMARY KEY,
    source_url       text         NOT NULL,
    nation           varchar(30)  NOT NULL,
    release_time     datetime     NOT NULL,
    institution      text         NULL,
    field            varchar(100) NULL,
    language         varchar(50)  NOT NULL,
    keywords         text         NULL,
    original_title   text         NOT NULL,
    translated_title text         NULL,
    abstract         text         NULL,
    file_url         text         NULL,
    original_file    int          NULL,
    format_file      int          NULL,
    translated_file  int          NULL,
    checked_file     int          NULL,
    `use`            tinyint(1)   NULL,
    recommend        tinyint(1)   NULL,
    `rank`           float        NULL,
    CONSTRAINT policy_text_ibfk_1
        FOREIGN KEY (original_file) REFERENCES file (id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT policy_text_ibfk_2
        FOREIGN KEY (format_file) REFERENCES file (id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT policy_text_ibfk_3
        FOREIGN KEY (translated_file) REFERENCES file (id)
            ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT policy_text_ibfk_4
        FOREIGN KEY (checked_file) REFERENCES file (id)
            ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE INDEX ix_policy_text_checked_file
    ON policy_text (checked_file);

CREATE INDEX ix_policy_text_format_file
    ON policy_text (format_file);

CREATE INDEX ix_policy_text_original_file
    ON policy_text (original_file);

CREATE INDEX ix_policy_text_translated_file
    ON policy_text (translated_file);

CREATE FULLTEXT INDEX policy_origin_title_index
    ON policy_text (original_title);




CREATE TABLE user
(
    id            int AUTO_INCREMENT
        PRIMARY KEY,
    username      text NOT NULL,
    password_hash text NOT NULL,
    role_id       int  NOT NULL
);

INSERT INTO user (id, username, password_hash, role_id) VALUES (1, 'admin', 'pbkdf2:sha256:150000$MQlyC7eF$2a941bd0aebd2f1a99372f6c47ba8e3084dfb36246371e142b32b3c103636a48', 1);
INSERT INTO user (id, username, password_hash, role_id) VALUES (3, 'super', 'pbkdf2:sha256:150000$MQlyC7eF$2a941bd0aebd2f1a99372f6c47ba8e3084dfb36246371e142b32b3c103636a48', 0);
INSERT INTO user (id, username, password_hash, role_id) VALUES (4, 'common', 'pbkdf2:sha256:150000$MQlyC7eF$2a941bd0aebd2f1a99372f6c47ba8e3084dfb36246371e142b32b3c103636a48', 2);








INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (78, 1, '5G Supply Chain Diversification Strategy', 'origin_5d56a9c569d69baadcc0c061f93ec8af.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (79, 3, '5 g供应链的多元化战略
', 'trans_5d56a9c569d69baadcc0c061f93ec8af.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (87, 1, 'Competition document: Countering Drones - Finding and neutralising small UAS threats Phase 2', 'origin_35556cbf054d8511f0679bcb7bf40cb4.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (88, 3, '文档:竞争对抗无人机——发现和中和小型无人机威胁第二阶段
', 'trans_35556cbf054d8511f0679bcb7bf40cb4.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (97, 1, 'Position statement on future of flight', 'origin_ebaca02657d71acc18dc8f61b4be962b.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (98, 3, '立场声明飞行的未来
', 'trans_ebaca02657d71acc18dc8f61b4be962b.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (112, 1, 'An inspection of British Transport Police’s ability to minimise disruption on the rail network', 'origin_dca19187dac220b179281e28b1cd7ad6.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (113, 3, '英国交通警察检查的能力减少中断的铁路网络
', 'trans_dca19187dac220b179281e28b1cd7ad6.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (114, 1, 'Technology innovation in government survey', 'origin_34eaff0b97fcbfb137ce9ae03c53e5e9.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (115, 3, '技术创新在政府调查
', 'trans_34eaff0b97fcbfb137ce9ae03c53e5e9.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (116, 1, 'Counter-Unmanned Aircraft Strategy (HTML)', 'origin_d705393e3eb19932be73c1c616dd89c7.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (117, 3, 'Counter-Unmanned飞机策略(HTML)
', 'trans_d705393e3eb19932be73c1c616dd89c7.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (121, 1, 'Ofsted''s innovation and regulation plan', 'origin_eab953d11b7dddf4c54ab8e0450bd32e.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (122, 3, 'Ofsted的创新和监管计划
', 'trans_eab953d11b7dddf4c54ab8e0450bd32e.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (132, 1, 'Regulation for the Fourth Industrial Revolution', 'origin_cefea4fb31e0e90b56cb2bf76eddd54f.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (133, 3, '监管的第四次工业革命
', 'trans_cefea4fb31e0e90b56cb2bf76eddd54f.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (141, 1, 'Science Advisory Council position statement: hyperloop', 'origin_f49965c0cca3731bf67311b8deca39aa.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (142, 3, '科学顾问委员会的立场声明:hyperloop
', 'trans_f49965c0cca3731bf67311b8deca39aa.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (159, 1, 'Government Technology Innovation Strategy', 'origin_e190f3d45127d15dab692aac894d1b2f.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (160, 3, '政府技术创新战略
', 'trans_e190f3d45127d15dab692aac894d1b2f.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (179, 1, 'Competition document: Biosensing across wide areas', 'origin_649529fe6cad7c55dc0c1ee6dbfc9619.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (209, 1, 'Competition Summary Document: Advanced Vision for 2020 and Beyond', 'origin_cbeb8df042e7edf4e9c493adb90846cd.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (235, 1, 'Competition Document: A Joint Effort – Integrating Advanced Materials onto Military Platforms', 'origin_8220e097a82f7840ec9f39d37d8f8ea4.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (264, 1, 'Competition document: predictive cyber analytics phase 2', 'origin_0090b7f7daea86ab3d187c6374f814b6.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (1712, 1, 'Competition document: windfarm mitigation for UK Air Defence', 'origin_621bf5dca0faf07a3ed294629d64f864.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (1724, 1, 'Competition summary: ‘Take Cover!’ Lightweight rapidly deployable protection on the front-line through Field Fortifications', 'origin_8e63e0afb68cb585e4f5999e084b7386.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (2312, 1, 'Advanced Manufacturing Materials competition: phases 2A and 2B successful projects', 'origin_022c77728d15c1269d48b45c819e18bb.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (2494, 1, 'Competition document: intelligent ship - the next generation', 'origin_aed57ccdb2f4052cb84e0ad4f1ffe3d0.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (2717, 1, 'Behavioural Analytics for Defence and Security', 'origin_d030e5e4a95b2eb23b26da87e29035aa.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (2755, 1, 'UK strategy for agricultural technologies: executive summary', 'origin_5ef8366f39ded9e19b70e87367e507ce.txt', 'HTML', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6930, 2, '5G Supply Chain Diversification Strategy', 'format_5d56a9c569d69baadcc0c061f93ec8af.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6934, 2, 'Competition document: Countering Drones - Finding and neutralising small UAS threats Phase 2', 'format_35556cbf054d8511f0679bcb7bf40cb4.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6939, 2, 'Position statement on future of flight', 'format_ebaca02657d71acc18dc8f61b4be962b.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6944, 2, 'An inspection of British Transport Police’s ability to minimise disruption on the rail network', 'format_dca19187dac220b179281e28b1cd7ad6.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6945, 2, 'Technology innovation in government survey', 'format_34eaff0b97fcbfb137ce9ae03c53e5e9.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6946, 2, 'Counter-Unmanned Aircraft Strategy (HTML)', 'format_d705393e3eb19932be73c1c616dd89c7.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6948, 2, 'Ofsted''s innovation and regulation plan', 'format_eab953d11b7dddf4c54ab8e0450bd32e.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6953, 2, 'Regulation for the Fourth Industrial Revolution', 'format_cefea4fb31e0e90b56cb2bf76eddd54f.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6957, 2, 'Science Advisory Council position statement: hyperloop', 'format_f49965c0cca3731bf67311b8deca39aa.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6964, 2, 'Government Technology Innovation Strategy', 'format_e190f3d45127d15dab692aac894d1b2f.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (6978, 2, 'Competition document: Biosensing across wide areas', 'format_649529fe6cad7c55dc0c1ee6dbfc9619.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7002, 2, 'Competition Summary Document: Advanced Vision for 2020 and Beyond', 'format_cbeb8df042e7edf4e9c493adb90846cd.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7024, 2, 'Competition Document: A Joint Effort – Integrating Advanced Materials onto Military Platforms', 'format_8220e097a82f7840ec9f39d37d8f8ea4.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7050, 2, 'Competition document: predictive cyber analytics phase 2', 'format_0090b7f7daea86ab3d187c6374f814b6.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7706, 2, 'Competition document: windfarm mitigation for UK Air Defence', 'format_621bf5dca0faf07a3ed294629d64f864.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7710, 2, 'Competition summary: ‘Take Cover!’ Lightweight rapidly deployable protection on the front-line through Field Fortifications', 'format_8e63e0afb68cb585e4f5999e084b7386.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7933, 2, 'Advanced Manufacturing Materials competition: phases 2A and 2B successful projects', 'format_022c77728d15c1269d48b45c819e18bb.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (7989, 2, 'Competition document: intelligent ship - the next generation', 'format_aed57ccdb2f4052cb84e0ad4f1ffe3d0.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (8075, 2, 'Behavioural Analytics for Defence and Security', 'format_d030e5e4a95b2eb23b26da87e29035aa.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (8104, 2, 'UK strategy for agricultural technologies: executive summary', 'format_5ef8366f39ded9e19b70e87367e507ce.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10011, 3, 'Competition document: Biosensing across wide areas', 'trans_649529fe6cad7c55dc0c1ee6dbfc9619.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10029, 3, 'Competition Summary Document: Advanced Vision for 2020 and Beyond', 'trans_cbeb8df042e7edf4e9c493adb90846cd.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10042, 3, 'Competition Document: A Joint Effort – Integrating Advanced Materials onto Military Platforms', 'trans_8220e097a82f7840ec9f39d37d8f8ea4.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10054, 3, 'Competition document: predictive cyber analytics phase 2', 'trans_0090b7f7daea86ab3d187c6374f814b6.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10553, 3, 'Competition document: windfarm mitigation for UK Air Defence', 'trans_621bf5dca0faf07a3ed294629d64f864.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10557, 3, 'Competition summary: ‘Take Cover!’ Lightweight rapidly deployable protection on the front-line through Field Fortifications', 'trans_8e63e0afb68cb585e4f5999e084b7386.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10751, 3, 'Advanced Manufacturing Materials competition: phases 2A and 2B successful projects', 'trans_022c77728d15c1269d48b45c819e18bb.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10803, 3, 'Competition document: intelligent ship - the next generation', 'trans_aed57ccdb2f4052cb84e0ad4f1ffe3d0.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10875, 3, 'Behavioural Analytics for Defence and Security', 'trans_d030e5e4a95b2eb23b26da87e29035aa.txt', 'txt', '0', null, null, 0);
INSERT INTO file (id, filetype, name, savename, extension, size, create_time, update_time, download) VALUES (10897, 3, 'UK strategy for agricultural technologies: executive summary', 'trans_5ef8366f39ded9e19b70e87367e507ce.txt', 'txt', '0', null, null, 0);












INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (68, 'https://www.gov.uk/government/publications/technology-innovation-in-government-survey', 'UK', '2018-08-20 00:00:00', 'Government Digital Service', 'Government', 'English', null, 'Technology innovation in government survey', '技术创新在政府调查
', '
<p>This work was carried out in 2017, led by the Government Digital Service (GDS).</p>
<p>You can access details of projects and technologies by looking at <a class="govuk-link" href="https://www.gov.uk/government/publications/government-innovation-and-emerging-technology-underlying-data-set">the underlying data and visualisation that supports this work</a>.</p>
', 'https://www.gov.uk/government/publications/technology-innovation-in-government-survey/technology-innovation-in-government-survey', 114, 6945, 115, null, null, null, 309);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (94, 'https://www.gov.uk/government/publications/the-government-technology-innovation-strategy', 'UK', '2019-06-10 00:00:00', 'Government Digital Service, Cabinet Office, and The Rt Hon Oliver Dowden CBE MP', 'Public services', 'English', null, 'Government Technology Innovation Strategy', '政府技术创新战略
', '
<p>This strategy sets out the foundations needed for government to innovate through emerging technologies. It provides a framework for departments to use as they make plans for digital, data and technology ahead of the next spending review.</p>
<p>It has 3 sections:</p>
<ul>
<li>people, establishing technical skills and creating innovative leaders and culture</li>
<li>process, which includes help with funding experimentation and innovative procurement</li>
<li>data and technology, including accessing and sharing useful data, how we can tackle legacy technology and updating standards and guidance</li>
</ul>
', 'https://www.gov.uk/government/publications/the-government-technology-innovation-strategy/the-government-technology-innovation-strategy', 159, 6964, 160, null, null, null, 288);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (57, 'https://www.gov.uk/government/publications/review-of-future-of-flight-2017', 'UK', '2018-09-18 00:00:00', 'Department for Transport', 'Transport', 'English', null, 'Review of future of flight 2017', '回顾2017航班的未来
', '
<p>States the position of the <a class="govuk-link" href="https://www.gov.uk/government/groups/dft-science-advisory-council">Department for Transport’s (<abbr title="Department for Transport">DfT</abbr>’s) Science Advisory Council</a> on the future of flight.</p>
<p>The document includes:</p>
<ul>
<li>an overview of how technology is changing the aviation sector</li>
<li>the considerations and challenges for these disruptive technologies</li>
<li>recommendations on areas for <abbr title="Department for Transport">DfT</abbr> to consider for future of flight technology</li>
</ul>
', 'https://www.gov.uk/government/publications/review-of-future-of-flight-2017/position-statement-on-future-of-flight', 97, 6939, 98, null, null, null, 140);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (78, 'https://www.gov.uk/government/publications/regulation-for-the-fourth-industrial-revolution', 'UK', '2019-06-11 00:00:00', 'Department for Business, Energy & Industrial Strategy', 'Business and industry', 'English', null, 'Regulation for the Fourth Industrial Revolution', '监管的第四次工业革命
', '
<p>The measures include:</p>
<ul>
<li>a new Regulatory Horizon Council to advise government on rules and regulations that may need to change to keep pace with technology</li>
<li>a digital Regulation Navigator to help businesses find their way through the regulatory landscape and bring their ideas to market</li>
<li>a review of the Regulators’ Pioneer Fund, which backs projects that are testing new technology in partnership with the regulators in a safe but innovative environment</li>
<li>a partnership with the World Economic Forum to shape global rules on innovative products and services</li>
</ul>
', 'https://www.gov.uk/government/publications/regulation-for-the-fourth-industrial-revolution/regulation-for-the-fourth-industrial-revolution', 132, 6953, 133, null, null, null, 116);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (83, 'https://www.gov.uk/government/publications/hyperloop-technology-review', 'UK', '2017-11-09 00:00:00', 'Department for Transport', 'Transport', 'English', null, 'Hyperloop technology review', 'Hyperloop技术评论
', '
<p>States the position of the <a class="govuk-link" href="https://www.gov.uk/government/groups/dft-science-advisory-council">Department for Transport’s Science Advisory Council</a> on emerging hyperloop technology.</p>
<p>It includes:</p>
<ul>
<li>a short analysis of the potential impact</li>
<li>a summary of the risks</li>
<li>ideas around appropriate steps the department might take to react to the development of this potentially disruptive new technology</li>
</ul>
', 'https://www.gov.uk/government/publications/hyperloop-technology-review/science-advisory-council-position-statement-hyperloop', 141, 6957, 142, null, null, null, 85);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (2243, 'https://www.gov.uk/government/publications/nuclear-innovation-programme-advanced-manufacturing-and-materials-competition-phase-2-successful-projects', 'UK', '2020-07-10 00:00:00', 'Department for Business, Energy & Industrial Strategy', 'Environment', 'English', null, 'Nuclear innovation programme: advanced manufacturing and materials competition, Phase 2 - successful projects', null, '
<p>Advanced manufacturing and materials (AMM) Phase 2 is a £20 million investment programme and focuses on increasing the manufacturing or technology readiness levels of technologies, including those established in Phase 1, towards demonstration and commercialisation.</p>
<p>Phase 2 is output led. It will produce a technology demonstrator or a number of demonstrators that include advanced manufacturing or construction techniques; incorporating and developing the learning and technologies from the Phase 1 funded programme.</p>
<p>Demonstrations will involve trial builds (or equivalent) including one or more of the technologies funded in Phase 1. These will be relevant to factory-build, modular and advanced construction, and digital engineering execution and assurance. The techniques could then be applied to the build, maintenance and decommissioning of a nuclear sites as well as future technologies.</p>
<p>The competition is closed for new applications. Details of the competition’s aims and objectives can be found in the <a class="govuk-link" href="https://www.gov.uk/government/publications/nuclear-innovation-programme-advanced-manufacturing-and-materials-phase-2">competition guidance</a>.</p>
', 'https://www.gov.uk/government/publications/nuclear-innovation-programme-advanced-manufacturing-and-materials-competition-phase-2-successful-projects/advanced-manufacturing-materials-competition-phases-2a-and-2b-successful-projects', 2312, 7933, 10751, null, null, null, 66);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (47, 'https://www.gov.uk/government/publications/5g-supply-chain-diversification-strategy', 'UK', '2020-11-30 00:00:00', 'Department for Digital, Culture, Media & Sport', 'Business and industry', 'English', null, '5G Supply Chain Diversification Strategy', '5 g供应链的多元化战略
', '
<p>The 5G supply chain diversification strategy will deliver lasting and meaningful change in the 5G supply chain and pave the way for a vibrant, innovative and dynamic market.</p>
<p>Within it we have set out our long-term vision for a healthy supply market, which is characterised by the principles of openness, flexibility and diversity. This means building an environment where competition and innovation bring forward new deployment models based on open interfaces and interoperable standards; where networks are flexible, built on a best of breed approach and made up of an array of suppliers; and where security standards are adopted by all operators and suppliers to ensure the robustness and resilience of our networks.</p>
<p>For any queries, please email: <a class="govuk-link" href="mailto:5g-diversification-strategy@dcms.gov.uk">5g-diversification-strategy@dcms.gov.uk</a>.</p>
', 'https://www.gov.uk/government/publications/5g-supply-chain-diversification-strategy/5g-supply-chain-diversification-strategy', 78, 6930, 79, null, null, null, 62);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (69, 'https://www.gov.uk/government/publications/uk-counter-unmanned-aircraft-strategy', 'UK', '2019-10-21 00:00:00', 'Home Office', 'Crime, justice and law', 'English', null, 'UK Counter-Unmanned Aircraft Strategy', '英国Counter-Unmanned飞机策略
', '
<p>The rapid development of drone technology presents significant commercial and leisure opportunities. However, drones can also be used to facilitate and commit crimes, and if flown recklessly or negligently can pose a risk to public safety.</p>
<p>The UK Counter-Unmanned Aircraft Strategy sets out our approach to mitigating the highest-harm risks to the UK resulting from the illegal use of aerial drones.</p>
<p>These include:</p>
<ul>
<li>facilitating terrorist attacks</li>
<li>facilitating crime, especially in our prisons</li>
<li>disrupting critical national infrastructure (CNI)</li>
</ul>
', 'https://www.gov.uk/government/publications/uk-counter-unmanned-aircraft-strategy/table', 116, 6946, 117, null, null, null, 61);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (2425, 'https://www.gov.uk/government/publications/competition-intelligent-ship-the-next-generation', 'UK', '2019-06-12 00:00:00', 'Defence and Security Accelerator, Defence Science and Technology Laboratory, and Ministry of Defence', 'Defence and armed forces', 'English', null, 'Competition: intelligent ship - the next generation', null, '
<div class="call-to-action">
<p>Please be aware that letters of support are not a submission requirement for this competition. Proposals will not be marked down for not including of a letter of support.</p>
</div>
<p>This Defence and Security Accelerator (DASA) competition is seeking proposals for novel and innovative technologies, approaches and enablers that could revolutionise decision making, mission planning and automation in military platforms beyond 2030.</p>
<p>These proposals must reflect a situation of ever growing data and information flow, evolving threats and the need to operate within a future operating environment.  This competition is initially seeking low technology readiness level (TRL), high risk and innovative options for a revolutionary, not evolutionary, change to future military capability.</p>
<p>Phase 1 has an initial £1M to fund multiple innovative proposals (£100K limit per proposal).  Future phases will aim to create suitable evaluation environments and to integrate technologies with each other. This demonstration and integration of the projects will be developed under continuing work within future phases of this project, with additional funding of up to £3M, depending on the outcomes of the initial phase.</p>
<p>The human-machine interfaces will also be an important part of this work and will assist stakeholders to envision how this type of intelligent automation can be interfaced with military systems in the future.</p>
<p>The competition will close at midday BST on 23 July 2019.</p>
', 'https://www.gov.uk/government/publications/competition-intelligent-ship-the-next-generation/competition-document-intelligent-ship-the-next-generation', 2494, 7989, 10803, null, null, null, 43);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (72, 'https://www.gov.uk/government/publications/ofsted-innovation-and-regulation', 'UK', '2017-03-27 00:00:00', 'Ofsted', 'Corporate information', 'English', null, 'Ofsted: innovation and regulation', 'Ofsted:创新和监管
', '
<p>This document is one of a suite of plans on innovation and regulation being published by UK regulators in spring 2017 as part of our commitment to better regulation.</p>
<p>This suite of plans follows on from a commitment in <a class="govuk-link" href="https://www.gov.uk/government/publications/fixing-the-foundations-creating-a-more-prosperous-nation">the government’s Productivity Plan</a>. They complement the government’s approach to develop a modern <a class="govuk-link" href="https://www.gov.uk/government/policies/industrial-strategy">Industrial Strategy for Britain</a>.</p>
', 'https://www.gov.uk/government/publications/ofsted-innovation-and-regulation/ofsteds-innovation-and-regulation-plan', 121, 6948, 122, null, null, null, 41);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (67, 'https://www.gov.uk/government/publications/ability-of-the-british-transport-police-to-minimise-disruption-on-the-rail-network', 'UK', '2020-04-27 00:00:00', 'Department for Transport, British Transport Police Authority, and HM Inspectorate of Constabulary and Fire & Rescue Services', 'Transport', 'English', null, 'Ability of the British Transport Police to minimise disruption on the rail network', '英国交通警察的能力,以尽量减少中断的铁路网络
', '
<p>In April 2018 <abbr title="Her Majesty''s Inspectorate of Constabulary and Fire and Rescue Services">HMICFRS</abbr> were commissioned by the Minister of State for Transport to inspect
British Transport Police (<abbr title="British Transport Police">BTP</abbr>) and assess the force’s ability to work with the rail industry to minimise disruption on the network.</p>
<p>The report looks at:</p>
<ul>
<li>how well the force aligns its policing priorities with those of the industry, while
maintaining its operational independence</li>
<li>how well the force minimises the disruption to the railway network caused by
trespass, fatalities, cable theft and other police-related matters</li>
</ul>
', 'https://www.gov.uk/government/publications/ability-of-the-british-transport-police-to-minimise-disruption-on-the-rail-network/an-inspection-of-british-transport-polices-ability-to-minimise-disruption-on-the-rail-network', 112, 6944, 113, null, null, null, 40);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (2686, 'https://www.gov.uk/government/publications/uk-agricultural-technologies-strategy', 'UK', '2013-07-22 00:00:00', 'Department for Business, Innovation & Skills, Department for Environment, Food & Rural Affairs, and Department for International Development', 'Environment', 'English', null, 'UK agricultural technologies strategy', null, '
<p>This strategy set out for the first time how the government, science researchers and the food and farming industry will build on the strengths of the <abbr title="United Kingdom">UK</abbr> agricultural technologies sector. It aimed to:</p>
<ul>
<li>improve the translation of research into practice through a £70 million government investment in an Agri-Tech Catalyst, a single fund for projects</li>
<li>increase support to develop, adopt and exploit new technologies and processes through £90 million of government funding for Centres for Agricultural Innovation</li>
<li>help the <abbr title="United Kingdom">UK</abbr> exploit the potential of data and informatics and become a global centre of excellence by establishing a Centre for Agricultural Informatics and Metrics of Sustainability</li>
<li>provide stronger leadership for the sector through the Leadership Council, giving industry a stronger and more cohesive voice with government and the science researchers</li>
<li>build a stronger skills base to attract and retain a workforce who are expert in developing and applying technologies from the
laboratory to the farm</li>
<li>increase understanding of what is being spent and where to increase alignment of industry research funding with public sector spend</li>
<li>increase <abbr title="United Kingdom">UK</abbr> export and inward investment performance through targeted sector support</li>
</ul>
<p>The <abbr title="United Kingdom">UK</abbr> strategy for agricultural technologies is part of the government’s <a class="govuk-link" href="https://www.gov.uk/government/policies/using-industrial-strategy-to-help-the-uk-economy-and-business-compete-and-grow">industrial strategy</a>.</p>
<p>The agricultural technologies infographic is available in other formats from Flickr: <a class="govuk-link" href="http://www.flickr.com/photos/bisgovuk/sets/72157633021669313/" rel="external">Industrial strategy sector infographics</a></p>
<h2 id="investment-in-the-agri-tech-sector-an-opportunity-for-you-to-participate">Investment in the Agri-Tech sector: an opportunity for you to participate</h2>
<p>The gap in translating high quality agricultural research into practical applications is an important theme in the strategy. The government will invest £160 million to strengthen existing and develop innovative new collaborations between public and private sector organisations.</p>
<p>The public were able to shape the collaborative research in this initiative. We sought feedback on identifying areas that offer the greatest potential for business engagement, to maximise translating research into better productivity and wider growth opportunities.</p>
<p>We have published a review of the feedback. This document also serves as the basis for further industry engagement in the future. It is purely for information, and does not set out new policy.</p>
', 'https://www.gov.uk/government/publications/uk-agricultural-technologies-strategy/uk-agricultural-technologies-strategy-executive-summary', 2755, 8104, 10897, null, null, null, 37);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (110, 'https://www.gov.uk/government/publications/competition-biosensing-across-wide-areas', 'UK', '2020-04-06 00:00:00', 'Defence and Security Accelerator, Defence Science and Technology Laboratory, and Ministry of Defence', 'Defence and armed forces', 'English', null, 'Competition: Biosensing across wide areas', null, '
<p>This Defence and Security Accelerator (DASA) competition is seeking proposals for innovative technologies that provide an improved way to rapidly detect and locate hazardous biological agents in the field for the benefit of defence and security operations.</p>
<p>Please note this is a Phase 2 competition of a multi-phase theme. It is not compulsory to have been involved in Phase 1 to apply. You should however make yourself aware of the <a class="govuk-link" href="https://www.gov.uk/government/publications/competition-summary-biosensing-across-wide-areas/competition-document-biosensing-across-wide-areas">previous competition</a> and the <a class="govuk-link" href="https://www.gov.uk/government/publications/accelerator-funded-contracts/accelerator-funded-contracts-1-april-2018-to-31-march-2019#biosensing-across-wide-areas">proposals we funded</a>.</p>
<p>Proposals will need to deliver a higher level of maturity than achieved in Phase 1. We expect the starting <a class="govuk-link" href="https://www.gov.uk/guidance/defence-and-security-accelerator-terms-and-conditions-and-contract-guidance#what-dasa-funds">Technology Readiness Level (TRL)</a> of the innovation to be TRL 3. By the end of the project, we expect the innovation to be sufficiently developed to achieve approximately TRL 4 – 5.</p>
<p>£700k is available to fund Phase 2, which closes for submissions on Monday 15 June 2020 at midday BST.</p>
', 'https://www.gov.uk/government/publications/competition-biosensing-across-wide-areas/competition-document-biosensing-across-wide-areas', 179, 6978, 10011, null, null, null, 36);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (140, 'https://www.gov.uk/government/publications/competition-advanced-vision-for-2020-and-beyond', 'UK', '2019-07-18 00:00:00', 'Defence and Security Accelerator and Defence Science and Technology Laboratory', 'Scientific research and development', 'English', null, 'Competition:  Advanced Vision for 2020 and Beyond', null, '
<div class="call-to-action">
<p>Further 1-to-1 teleconference sessions are now available. This is an opportunity to ask questions about the competition to the technical team and DASA. These will be held on 17 October 2019 and can be booked through <a class="govuk-link" href="https://www.eventbrite.co.uk/e/advanced-vision-for-2020-and-beyond-1-to-1s-tickets-74813167197" rel="external">Eventbrite</a>.</p>
</div>
<p>This Defence and Security Accelerator (DASA) competition is seeking proposals to develop and demonstrate a number of novel technologies or applications in the area of Electro-Optics and Infrared (EOIR) to address the future need for highly capable and affordable sensors.  EOIR sensors are a key military capability used for surveillance, reconnaissance, target acquisition, threat warning, target detection and more. The ever evolving nature of military operations means that we wish to invest in novel and resilient technologies that can function in contested/congested environments, that will extend the range, lower the cost and size, and expand the range of targets that can be addressed by EOIR sensors.</p>
<p>Total funding of £2.5m is expected to be available over 2 phases to fund multiple projects in each phase.
This competition is expected to open in August 2019.</p>
<p>In parallel to this competition, the <a class="govuk-link" href="https://www.gov.uk/government/publications/competition-autonomy-in-challenging-environments">Autonomy in Challenging Environments competition</a> is seeking novel and innovative technologies to improve the capability of autonomous military systems in challenging environments for which sensor technology may be applicable. If a proposal is submitted to both competitions, it should clearly outline any duplication of costs and works. This competition will be holding a dial in event, further information can be found on <a class="govuk-link" href="https://www.eventbrite.co.uk/e/autonomy-in-challenging-environments-dial-in-tickets-69167262143" rel="external">Eventbrite</a>.</p>
<p>Queries should be sent to <a class="govuk-link" href="mailto:accelerator@dstl.gov.uk">accelerator@dstl.gov.uk</a>.</p>
', 'https://www.gov.uk/government/publications/competition-advanced-vision-for-2020-and-beyond/competition-summary-document-advanced-vision-for-2020-and-beyond', 209, 7002, 10029, null, null, null, 36);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (1655, 'https://www.gov.uk/government/publications/competitiontake-coverlightweight-rapidly-deployable-protection-on-the-front-line-through-field-fortifications', 'UK', '2018-08-01 00:00:00', 'Defence and Security Accelerator, Ministry of Defence, and Defence Science and Technology Laboratory', 'Defence and armed forces', 'English', null, 'Competition: ''Take Cover!’ Lightweight rapidly deployable protection on the front-line through Field Fortifications', null, '
<p>Within defence and security, protection of personnel is a priority area and deployment of rapid protection solutions for dismounted (on-foot) troops on the front-line is of high importance.</p>
<p>This DASA competition seeks proposals to access recent innovations in both materials science and design technologies to provide advanced protection solutions for small groups of front-line troops from impacts such as that from ballistic, blast and directed energy threats.</p>
<p>DASA are interested in proof-of-concept technologies which can be integrated into a single system during later competition phases.</p>
<p>There is funding of up to £600k available in Phase 1 of the competition. It is anticipated that significant additional funding will be available for further phases.</p>
<div class="call-to-action">
<p>This competition is now open and details are available in the <a class="govuk-link" href="https://www.gov.uk/government/publications/competitiontake-coverlightweight-rapidly-deployable-protection-on-the-front-line-through-field-fortifications/competition-document-take-cover-lightweight-rapidly-deployable-protection-on-the-front-line-through-field-fortifications">competition document</a>.</p>
</div>
<p>Queries should be sent to <a class="govuk-link" href="mailto:accelerator@dstl.gov.uk">accelerator@dstl.gov.uk</a>.</p>
', 'https://www.gov.uk/government/publications/competitiontake-coverlightweight-rapidly-deployable-protection-on-the-front-line-through-field-fortifications/competition-summary-take-cover-lightweight-rapidly-deployable-protection-on-the-front-line-through-field-fortifications', 1724, 7710, 10557, null, null, null, 33);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (1643, 'https://www.gov.uk/government/publications/windfarm-mitigation-for-uk-air-defence', 'UK', '2020-03-05 00:00:00', 'Defence and Security Accelerator, Ministry of Defence, and Department for Business, Energy & Industrial Strategy', 'Manufacturing', 'English', null, 'Windfarm Mitigation for UK Air Defence', null, '
<p>This Defence and Security Accelerator (DASA) competition is seeking proposals that can provide future offshore windfarm mitigation for UK Air Defence surveillance; including alternative technologies that could fill or remove gaps in radar coverage.</p>
<p>The competition is funded by the <a class="govuk-link" href="https://www.gov.uk/government/organisations/department-for-business-energy-and-industrial-strategy">Department for Business, Energy, and Industrial Skills’</a> (BEIS) Science and Innovation for Climate and Energy (SICE) portfolio; and is undertaken in partnership with the <a class="govuk-link" href="https://www.raf.mod.uk/" rel="external">Royal Air Force</a> (RAF), the <a class="govuk-link" href="https://www.gov.uk/government/organisations/defence-science-and-technology-laboratory">Defence Science and Technology Laboratory</a> (Dstl), and the <a class="govuk-link" href="https://www.gov.uk/government/organisations/defence-and-security-accelerator">Defence and Security Accelerator</a> (DASA).</p>
<p>A total of up to £2m is available, intended to fund a number of contracts of up to £500k.</p>
<h5 id="the-competition-will-close-at-midday-gmt-on-17-april-2020">The competition will close at midday GMT on 17 April 2020.</h5>
<p>DASA will be holding a dial in briefing session and 1-1 slots to enable potential suppliers to ask questions:</p>
<p>26 March 2020 – A dial-in session providing further detail on the problem space and a chance to ask questions in an open forum. If you would like to participate, please register on the <a class="govuk-link" href="https://www.eventbrite.co.uk/e/windfarm-mitigation-dial-in-tickets-96056691149" rel="external">Dial in Eventbrite page</a>.</p>
<p>26 March 2020 – A series of 20 minute one-to-one teleconference sessions, giving you the opportunity to ask specific questions. If you would like to participate, please register on the <a class="govuk-link" href="https://www.eventbrite.co.uk/e/windfarm-mitigation-1-to-1-tickets-96057252829" rel="external">1-1s Eventbrite page</a>.</p>
<p>Additional date added</p>
<p>2 April 2020 – A series of 15 minute one-to-one teleconference sessions, giving you the opportunity to ask specific questions. If you would like to participate, please register on the <a class="govuk-link" href="https://www.eventbrite.co.uk/e/windfarm-mitigation-for-uk-air-defence-1-to-1s-tickets-101540887528" rel="external">1-1s Eventbrite page</a>.</p>
', 'https://www.gov.uk/government/publications/windfarm-mitigation-for-uk-air-defence/competition-document-windfarm-mitigation-for-uk-air-defence', 1712, 7706, 10553, null, null, null, 33);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (166, 'https://www.gov.uk/government/publications/a-joint-effort-integrating-advanced-materials-onto-military-platforms', 'UK', '2018-11-27 00:00:00', 'Defence and Security Accelerator', null, 'English', null, 'A Joint Effort – Integrating Advanced Materials onto Military Platforms', null, '
<div class="call-to-action">
<p>This Phase of the competition has now  closed, information on Phase 2 is available from  <a class="govuk-link" href="https://www.gov.uk/government/publications/a-joint-effort-phase-2">A Joint Effort - Integrating Advanced Material on military Platforms - Phase 2</a></p>
</div>
<p>Phase 1 of the campaign has £500k available through DASA to fund multiple proposals. It is anticipated that additional funding will be available for further phases. This campaign will be supported in Australia by the Australian Defence Science and Technology Group (DST Group) Next Generation Technologies Fund and Small Business Innovation Research for Defence (SBIRD) in a parallel competition with separate funding.</p>
<p>You can <a class="govuk-link" href="https://www.gov.uk/government/email-signup/new?email_signup%5Bfeed%5D=https://www.gov.uk/government/organisations/defence-and-security-accelerator.atom">sign up for alerts</a> on our news pages to keep up to date. You will need to register for the DASA <a class="govuk-link" href="https://www.us17.list-manage.com/subscribe?u=f2f4a3a978ac36da6423d10f8&amp;id=a74971af4e" rel="external">Submission Service to submit a proposal</a>.</p>
<p>Phase 1 will close for submission of proposals at midday on Friday 01 February 2019.</p>
<p>Queries should be sent to <a class="govuk-link" href="mailto:accelerator@dstl.gov.uk">accelerator@dstl.gov.uk</a></p>
', 'https://www.gov.uk/government/publications/a-joint-effort-integrating-advanced-materials-onto-military-platforms/competition-document-a-joint-effort-integrating-advanced-materials-onto-military-platforms', 235, 7024, 10042, null, null, null, 30);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (52, 'https://www.gov.uk/government/publications/countering-drones-finding-and-neutralising-small-uas-threats-phase-2', 'UK', '2020-05-12 00:00:00', 'Defence and Security Accelerator and Defence Science and Technology Laboratory', null, 'English', null, 'Countering Drones: Finding and neutralising small UAS threats - Phase 2', '打击无人机:发现和中和小无人机威胁——第二阶段
', '
<div class="call-to-action">
<h1 id="deadline-extended">DEADLINE EXTENDED</h1>
<p>In light of additional funding (total now £3M), the deadline for this competition will be extended by 10 days: proposals for funding to meet these challenges must be submitted by Friday, 31 July at midday (BST) via the DASA submission service for which you will be <a class="govuk-link" href="https://www.gov.uk/government/collections/defence-and-security-accelerator-submit-your-research-proposal">required to register</a>.</p>
</div>
<p>The Defence and Security Accelerator (DASA) is looking for innovative solutions to address the increasing UAS threat to the defence and security of UK both at home and abroad.</p>
<p>Please note this is the second phase of funding for a multi-phase competition. It is not compulsory to have been involved in previous phases to apply. You should however make yourself aware of the previous competition and the bids we funded. It is anticipated that work for this phase will reach higher maturity than work funded in Phase 1.</p>
', 'https://www.gov.uk/government/publications/countering-drones-finding-and-neutralising-small-uas-threats-phase-2/competition-document-countering-drones-finding-and-neutralising-small-uas-threats-phase-2', 87, 6934, 88, null, null, null, 30);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (2648, 'https://www.gov.uk/government/publications/competition-behavioural-analytics-for-defence-and-security', 'UK', '2018-10-11 00:00:00', 'Defence and Security Accelerator', null, 'English', null, 'Competition: Behavioural Analytics for Defence and Security', null, '
<p>DASA are looking for scientific and technological solutions that can provide context-specific insights into the ‘how’ and ‘why’ of individual, group and population behaviour, enabling predictions about how they are likely to act in the future. At this stage of the competition we are limiting the scope to theoretical development, methodological advancement and proof of concept research.</p>
<p>Phase 1 of this competition has £1.6 million available to fund multiple proposals. Additional funding is anticipated to be available for future phases of this competition.</p>
<p>This competition closes on Wednesday 5 December 2018 at midday.</p>
<p>Queries should be sent to <a class="govuk-link" href="mailto:accelerator@dstl.gov.uk">accelerator@dstl.gov.uk</a></p>
', 'https://www.gov.uk/government/publications/competition-behavioural-analytics-for-defence-and-security/behavioural-analytics-for-defence-and-security', 2717, 8075, 10875, null, null, null, 30);
INSERT INTO policy_text (id, source_url, nation, release_time, institution, field, language, keywords, original_title, translated_title, abstract, file_url, original_file, format_file, translated_file, checked_file, `use`, recommend, `rank`) VALUES (195, 'https://www.gov.uk/government/publications/competition-predictive-cyber-analytics-phase-2', 'UK', '2019-07-03 00:00:00', 'Defence and Security Accelerator and Defence Science and Technology Laboratory', 'Scientific research and development', 'English', null, 'Competition: predictive cyber analytics phase 2', null, '
<p>The Defence and Security Accelerator (DASA) is interested in technologies that can provide a proactive cyber defence capability in MOD’s fixed and deployed military environments to help counter and defeat future cyber threats.</p>
<p>This second phase seeks to further develop and enhance novel predictive approaches within the military cyber security domain. The work will allow MOD to better prepare for, respond to and mitigate the impact of cyber-attack.</p>
<p>Total funding of up to £850k is available in Phase 2 of this competition. We anticipate funding up to 3 research projects of up to 12 months’ duration. Applicants do not have to have applied to Phase 1 to be eligible, <a class="govuk-link" href="https://www.gov.uk/government/publications/predictive-cyber-analytics">details on Phase 1 can be found on our website</a>.</p>
<p>This competition is now open and will close at midday (BST) on Mon 12th Aug 2019.
Queries should be sent to <a class="govuk-link" href="mailto:accelerator@dstl.gov.uk">accelerator@dstl.gov.uk</a>.</p>
', 'https://www.gov.uk/government/publications/competition-predictive-cyber-analytics-phase-2/competition-document-predictive-cyber-analytics-phase-2', 264, 7050, 10054, null, null, null, 30);