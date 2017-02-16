from github import Github, GithubException, Label
from models import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from log import logger


g = Github('mljcisneros', '1b005490c2faea6eaeaa151b21e51548ad0cef98')

org = g.get_organization('melitest')


engine = create_engine('sqlite:///githubmelitest.sqlite')
models.Base.metadata.create_all(engine)
models.Base.metadata.bind = engine

DBsession = sessionmaker()
DBsession.bind = engine
session = DBsession()


def get_teams():
    """Cada request al api de github se durante la recorrida de la
    estructura teams."""
    try:
        teams = org.get_teams()
        for team in teams:
            save_team(team)
            save_dev_membership(team)

    except GithubException as e:
        logger.info(e.message)
        print (e.message)


def save_team(team_to_save):
    """Guarda el team en la base de datos.
       Team : Github.Team."""
    try:
        team = models.Team()
        team.name = team_to_save.name
        session.add(team)
        session.commit()
    except Exception as e:
        if (hasattr(e, 'message')):
            print (e.message)
        else:
            print (e)
        session.rollback()


def save_dev_membership(team):
    """Obtiene los miembros del equipo y los guarda
       en la base de datos.
       team es Github.Team."""
    try:
        for member in team.get_members():
            new_member = models.Member()
            new_member.team_id = team.name
            new_member.dev_id = member.login
            session.add(new_member)
            session.commit()
    except Exception as e:
        if (hasattr(e, 'message')):
            print (e.message)
        else:
            print (e)
        session.rollback()


def get_members(team):
    try:
        members = team.get_members()
        for member in members:
            save_dev(member)
    except GithubException as e:
        print (e.message)


def get_repos():
    try:
        repos = org.get_repos()
        for repo in repos:
            print (repo.name)
            print (repo.full_name)
            vuln = Label.Label()
            #vuln.name="vulnerabilty"
            #print (vuln.name)
            issues = repo.get_issues(labels=[vuln])
            for i in issues:
                print (i.title)
            # save_repo(repo)
    except Exception as e:
        print (e)

#def save_repo(repo):
#    try:
#        new_repo = models.Repo()
#        new_repo = repo.name
#
#    except:


""" Ver si esta en la organizacion.
Todos los miembros deben estar activos en ldap."""


def save_dev(dev_to_save):
    try:
        dev = models.Dev()
        dev.login = dev_to_save.login
        dev.name = dev_to_save.name
        session.add(dev)
        session.commit()
    except Exception as e:
        if (hasattr(e, 'message')):
            print (e.message)
        else:
            print (e)
        session.rollback()


def get_devs():
    all_devs = org.get_members()
    for dev in all_devs:
        save_dev(dev)

query = session.query(models.Team).all()


# get_devs()
# get_teams()
get_repos()


"""
issues se pueden buscar por vulnerabilty con el api
de search

O se pueden traer todos los issues de cada repo.
"""
def search_issues():
    """print issues."""
    query = g.search_issues("org:melitest label:vulnerability")

    for q in query:
        print (q.title)

        labels = q.get_labels()
        for label in labels:
            print (label.name)


# org.get_repo('seginf-leakmonitor')
# query = session.query(models.Dev).all()
#
# for q in query:
#     print q.name
