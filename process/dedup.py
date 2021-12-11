# -*- coding: utf-8 -*-

""" 
@author: Jin.Fish
@file: dedup.py
@version: 1.0
@time: 2021/08/18 16:51:46
@contact: jinxy@pku.edu.cn

去重复
# todo 能否run多次是一个问题
"""
from collections import Counter
from pprint import pprint
from process import File, PolicyText as Policy, db, Config
from disruptive import app
app.app_context().push()


def dedup_same_title():
    title_list = Policy.query.with_entities(Policy.original_title).filter(Policy.rank > Config.RANK_TH,
                                                                          Policy.original_title != None
                                                                          ).all()
    title_list = [t[0] for t in title_list]
    title_counter = Counter(title_list)
    dup_titles = list(filter(lambda x: title_counter[x] > 1, title_counter))
    remove_cnt = 0
    for t in dup_titles:
        p_list = Policy.query.filter(Policy.rank > Config.RANK_TH, Policy.original_title == t).all()
        print(f"{len(p_list)} | {t}")
        for idx, p in enumerate(p_list):  # type: Policy
            if idx == 0: continue
            p.use = False
            db.session.add(p)
            remove_cnt += 1
    db.session.commit()
    print(f"totally removed {remove_cnt}")


if __name__ == '__main__':
    dedup_same_title()


"""
log:
2 | Europe's future
2 | Study on innovation in higher education
2 | The Safer Affordable Fuel-Efficient (SAFE) Vehicles Rule for Model Years 2021-2026 Passenger Cars and Light Trucks
5 | National Defense Authorization Act for Fiscal Year 2020
2 | Legislative Branch Appropriations for Fiscal Year 2006
2 | Department of Defense Authorization for Appropriations for Fiscal Year 2006
2 | Implementation of the Provisions of the Energy Policy Act of 2005
2 | NATIONAL DEFENSE AUTHORIZATION ACT FOR FISCAL YEAR 2006
2 | NEW DIRECTION FOR ENERGY INDEPENDENCE, NATIONAL SECURITY, AND CONSUMER PROTECTION ACT
2 | STATEMENTS ON INTRODUCED BILLS AND JOINT RESOLUTIONS
13 | TEXT OF AMENDMENTS
2 | Energy Policy Act of 2002
2 | To amend the Elementary and Secondary Education Act of 1965, and for other purposes.
2 | Energy Policy Act of 2003
2 | An Act to improve learning and teaching by providing a national framework for education reform; to promote the research, consensus building, and systemic changes needed to ensure equitable educational opportunities and high levels of educational achievement for all American students; to provide a framework for reauthorization of all Federal education programs; to promote the development and adoption of a voluntary national system of skill standards and certifications; and for other purposes
2 | An Act to enhance energy conservation, research and development and to provide for security and diversity in the energy supply for the American people, and for other purposes.
4 | To amend the Elementary and Secondary Education Act of 1965, to reauthorize and make improvements to that Act, and for other purposes.
2 | Department of the Interior and Related Agencies Appropriations for Fiscal Year 2005
2 | Goals 2000: Educate America
2 | AMENDMENTS SUBMITTED
2 | CONFERENCE REPORT ON H.R. 2419, FOOD, CONSERVATION, AND ENERGY ACT OF 2008
2 | Energy and Water Development Appropriations for Fiscal Year 2010
2 | Loan Guarantee Program
4 | Protecting Cyberspace as a National Asset Act of 2010
2 | Commerce, Justice, Science, and Related Agencies Appropriations for Fiscal Year 2009
2 | Department of Defense Appropriations for Fiscal Year 2009
5 | NATIONAL DEFENSE AUTHORIZATION ACT FOR FISCAL YEAR 2011
5 | National Defense Authorization Act for Fiscal Year 2011
2 | Departments of Labor, Health and Human Services, and Education, and Related Agencies Appropriations for Fiscal Year 2011
3 | Department of Defense Authorization for Appropriations for Fiscal Year 2013 and the Future Years Defense Program
4 | Department of Defense Authorization for Appropriations for Fiscal Year 2014 and the Future Years Defense Program
3 | Department of Defense Authorization of Appropriations for Fiscal Year 2015 and the Future Years Defense Program
2 | Energy and Water Development Appropriations for Fiscal Year 2015
2 | NATIONAL DEFENSE AUTHORIZATION ACT FOR FISCAL YEAR 2014
5 | NATIONAL DEFENSE AUTHORIZATION ACT FOR FISCAL YEAR 2013
5 | National Defense Authorization Act for Fiscal Year 2013
2 | Workforce Investment Act of 2013
2 | STUDENT SUCCESS ACT
3 | Department of Defense Authorization for Appropriations for Fiscal Year 2017 and the Future Years Defense Program
2 | Advisory Committee on Automation in Transportation
2 | CYBER SECURITY
3 | Department of Defense Authorization for Appropriations for Fiscal Year 2016 and the Future Years Defense Program
2 | HIRE MORE HEROES ACT OF 2015
2 | Transportation and Housing and Urban Development, and Related Agencies Appropriations for Fiscal Year 2017
2 | Department of Defense Appropriations for Fiscal Year 2017
2 | Energy and Water Development Appropriations for Fiscal Year 2017
2 | Greenhouse Gas Emissions and Fuel Efficiency Standards for Medium- and Heavy-Duty Engines and Vehicles-Phase 2
4 | EVERY CHILD ACHIEVES ACT OF 2015
2 | FIVE PILLARS OF WHAT WE BELIEVE SAVES US
2 | Department of Defense Authorization for Appropriations for Fiscal Year 2019 and the Future Years Defense Program
2 | Department of Defense Appropriations for Fiscal Year 2018
5 | NATIONAL DEFENSE AUTHORIZATION ACT FOR FISCAL YEAR 2020
2 | AUTHORIZATION AND OVERSIGHT PLANS FOR ALL HOUSE COMMITTEES
4 | NATIONAL DEFENSE AUTHORIZATION ACT FOR FISCAL YEAR 2018
5 | FAA Reauthorization Act of 2018
3 | America's Transportation Infrastructure Act of 2019
4 | National Defense Authorization Act for Fiscal Year 2018
3 | Agriculture Improvement Act of 2018
2 | From Big Data to Cloud Computing: How IT is Creating a New Era of Disruptive Innovation
2 | Spurring Technological Innovation in America’s Legacy Sectors
totally removed 110
"""