from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Integer, Column, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()
# engine = create_engine(settings.MYSQL_ENGINE, echo=True)
engine = create_engine(
    'mysql+pymysql://root:root@localhost:3306/d3?charset=utf8', echo=True)


class SessionMaker(object):
    @classmethod
    def get_session(cls):
        session = sessionmaker(bind=engine)
        return session()


session = SessionMaker.get_session()


class Element(Base):
    __tablename__ = "element"

    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)

    skills = relationship('Skill', backref='element_skills')
    runes = relationship('Rune', backref='element_runes')

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), index=True)
    description = Column(String(400))
    unlock_level = Column(Integer)
    hit_percent = Column(Integer)
    icon = Column(String(200))
    ref = Column(String(200))

    # 元素关联
    # element_id = Column(Integer, ForeignKey('element.id'))
    # element = relationship("Element", back_populates="skills")
    element_id = Column(Integer, ForeignKey('element.id'))

    # 符文关联
    runes = relationship('Rune', backref='skill_runes')

    # 与职业关联
    job_id = Column(Integer, ForeignKey('job.id'))

    # 与技能种类关联
    skill_kind_id = Column(Integer, ForeignKey('skill_kind.id'))

    def __init__(self, **skill):
        for key in skill:
            if hasattr(self, key):
                setattr(self, key, skill[key])

    def __repr__(self):
        return self.name


class SkillKind(Base):
    __tablename__ = 'skill_kind'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    # 与技能关联
    skills = relationship('Skill', backref='skillkind_skill')

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name


class Rune(Base):
    __tablename__ = 'rune'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))
    description = Column(String(300))
    icon = Column(String(10))
    unlock_level = Column(Integer)
    proc_coefficient = Column(Integer)

    # 技能关联
    skill_id = Column(Integer, ForeignKey('skill.id'))
    # skill = relationship("Skill", back_populates="runes")

    # 元素关联
    element_id = Column(Integer, ForeignKey('element.id'))
    # element = relationship("Element", back_populates="runes")

    def __init__(self, **rune):
        for key in rune:
            if hasattr(self, key):
                setattr(self, key, rune[key])

    def __repr__(self):
        return self.name


class Job(Base):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    name = Column(String(20))

    # 与技能关联
    skills = relationship('Skill', backref='job_skills')

    def __repr__(self):
        return self.name

    def __init__(self, name):
        self.name = name

if __name__ == '__main__':
    Base.metadata.create_all(engine)
