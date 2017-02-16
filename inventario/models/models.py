from sqlalchemy.ext.declarative import declarative_base
# import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, Boolean

Base = declarative_base()


class Repo(Base):
    __tablename__ = "repository"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(255))
    update_date = Column(DateTime)
    create_date = Column(DateTime)
    repo_test = Column(Boolean)
    ambiente = Column(String(50))  # fury melicloud pci ,etc
    visibility = Column(String(50))
    stack = Column(String(50))  # Un tag ejemplo grails


class Dev(Base):
    __tablename__ = "developer"
    # __table_args__ = {'sqlite_autoincrement': True}
    # id = Column(Integer, primary_key=True)
    login = Column(String(255), primary_key=True)
    name = Column(String(255)) # algunos usuarios tienen
    account_role = Column(String(30)) # member / owner # parecido organization_status
    organization_status = Column(String(30)) # Miembro Activo / Externo / Ex Miembro.
    oficce = Column(String(30)) # pedido por Rocket para eventos de leak tendria utilidad


class Contribution(Base):
    """Representa la relacion entre devs y repos """
    __tablename__ = "contribution"
    dev_id = Column(String(255),
                    ForeignKey("developer.login"),
                    primary_key=True
                    )
    repo_id = Column(Integer,
                     ForeignKey("repository.id"),
                     primary_key=True
                     )
    cant_commits = Column(Integer)
    last_commit_date = Column(DateTime)
    fork = Column(String(100))
    permisos = Column(String(100))


class Member(Base):
    __tablename__ = "member"
    dev_id = Column(String(255),
                    ForeignKey("developer.login"),
                    primary_key=True
                    )
    team_id = Column(String(255),
                     ForeignKey("team.name"),
                     primary_key=True
                     )


class Team(Base):
    __tablename__ = "team"
    __table_args__ = {'sqlite_autoincrement': True}
    name = Column(String(255), primary_key=True)
    description = Column(String(255))

class Issue(Base):
    __tablename__ = "issue"
    __table_args__ = {'sqlite_autoincrement': True}
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(String(255))
