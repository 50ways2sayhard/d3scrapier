# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from d3scrapier.tools.path_tools import get_data_folder
from d3scrapier.models import session, Rune, Element, Skill, Job, SkillKind


class D3ScrapierPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline(object):
    def open_spider(self, spider):
        data_folder = get_data_folder()
        print('*'*50)
        print('Start serialize...')
        if spider.name != 'default':
            self.file = open(data_folder + '/' + spider.name + '.json', 'w')

    def close_spider(self, spider):
        print('*'*50)
        print('Finish serialize....')
        if spider.name != 'default':
            self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        if spider.name != 'default':
            self.file.write(line)
        return item


class SQLWriterPipeline(object):
    def process_item(self, item, spider):
        if item['item_type'] == 'skill':
            self.process_skill(item)

    def process_skill(self, item):
        s = item['descp']
        rs = item['runes']
        skill = session.query(Skill).filter(Skill.name == s['name']).first()
        if skill is not None:
            return
        
        # 处理技能
        # 职业
        job = session.query(Job).filter(Job.name == s['job']).first()
        if job is None:
            job = Job(s['job'])
            session.add(job)
        # 技能种类
        skillkind = session.query(SkillKind).filter(SkillKind.name == s['kind']).first()
        if skillkind is None:
            skillkind = SkillKind(s['kind'])
            session.add(job)
        # 元素
        element = session.query(Element).filter(Element.name == s['type']).first()
        if element is None:
            element = Element(s['type'])
            session.add(element)
        skill = Skill(**s)
        element.skills.append(skill)
        job.skills.append(skill)
        skillkind.skills.append(skill)
        session.add_all([element, job, skillkind])
        session.commit()

        # 处理符文
        for rune in rs:
            ele = session.query(Element).filter(Element.name == rune['element']).first()
            if ele is None:
                ele = Element(rune['element'])
                session.add(ele)
                session.commit()
            r = Rune(**rune)
            ele.runes.append(r)
            skill.runes.append(r)
            session.add_all([r, ele])
        
        session.add(skill)
        session.commit()
    
    def close_spider(self, spider):
        session.close()
