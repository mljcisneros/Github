
# -*- coding: UTF-8 -*-

from github import Github, GithubException, Label
from models import models
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from log import logger
import sys
import traceback





org = g.get_organization('melitest')


engine = create_engine('sqlite:///githubmelitest.sqlite')
models.Base.metadata.create_all(engine)
models.Base.metadata.bind = engine

DBsession = sessionmaker()
DBsession.bind = engine
session = DBsession()

Enviroment = "DEBUG"



def log_exception(ex):
    if Enviroment == "DEBUG":
        if (hasattr(ex, 'message')):
            print (ex.message)
        else:
            print (ex)
        print ("stackTrace")
        traceback.print_exc(file=sys.stdout)





@try_except
def get_teams():
    """Cada request al api de github se durante la recorrida de la
    estructura teams."""
    teams = org.get_teams()
    for team in teams:
        save_team(team)
        save_dev_membership(team)

@try_except_db
def save_team(team_to_save):
    """Guarda el team en la base de datos.
       Team : Github.Team."""
    team = session.query(models.Team).\
                   get(team_to_save.name)
    if (team):
        return
    team = models.Team()
    team.name = team_to_save.name
    session.add(team)
    session.commit()



def save_dev_membership(team):
    """Obtiene los miembros del equipo y los guarda
       en la base de datos.
       team es Github.Team."""
    for member in team.get_members():
        query = session.query(models.Member).\
                        filter(models.Member.dev_id == member.login,
                               models.Member.team_id == team.name
                               )
        new_member = query.first()
        if (new_member):
            return
        new_member = models.Member()
        new_member.team_id = team.name
        new_member.dev_id = member.login
        session.add(new_member)
        session.commit()


@try_except
def get_members(team):
    members = team.get_members()
    for member in members:
        save_dev(member)


# Get last commit del repo. Fecha del commit
@try_except
def get_repos():
    repos = org.get_repos()
    for repo in repos:
        save_repo(repo)
        save_last_commit(repo)


def save_repo(repo):
    new_repo = session.query(models.Repo).get(repo.name)
    if (new_repo):
        return
    new_repo = models.Repo()
    new_repo.name = repo.name
    new_repo.create_date = repo.created_at
    new_repo.private = repo.private
    new_repo.description = repo.description

    session.add(new_repo)
    session.commit()

#    with open('file') as file:



def save_last_commit(repo):
    commits = repo.get_commits(since=repo.pushed_at)
    print (repo.name)
    query = session.query(models.Repo).\
                    filter(models.Repo.name == repo.name)
    if query:
        repo = query.first()
        for commit in commits:
            query = session.query(models.Commit).\
                            filter(models.Commit.html_url == commit.html_url)
            new_commit = query.first()
            if (new_commit):
                return
            new_commit = models.Commit()
            new_commit.date = commit.commit.author.date
            new_commit.html_url = commit.html_url
            new_commit.author = commit.author.login
            new_commit.repo_id = repo.id

            session.add(new_commit)
            session.commit()


#def get_issues():
    #vuln = Label.Label()
    #vuln.name="vulnerabilty"
    #print (vuln.name)
    #issues = repo.get_issues(labels=[vuln])
    #for i in issues:
    #    print (i.title)




""" Ver si esta en la organizacion.
Todos los miembros deben estar activos en ldap."""

@try_except_db
def save_dev(dev_to_save):
    dev = session.query(models.Dev).\
                  get(dev_to_save.login)
    if (dev):
        return
    dev = models.Dev()
    dev.login = dev_to_save.login
    dev.name = dev_to_save.name
    dev.account_role = dev_to_save.type
    session.add(dev)
    session.commit()

@try_except
def get_devs():
    all_devs = org.get_members()
    for dev in all_devs:
        save_dev(dev)


#testRepo = org.get_repo("testissues")
#create_security_labels(testRepo)
"""
issues se pueden buscar por vulnerabilty con el api
de search

O se pueden traer todos los issues de cada repo.
"""
def search_issues():
    """print issues."""
    issues = g.search_issues("org:melitest label:vulnerability")

    for q in query:
        print (q.title)

        labels = q.get_labels()
        for label in labels:
            print (label.name)

def create_security_labels(repo):
    labels={'high vulnerability':'b83040'}
    repo.create_label("")


get_devs()
get_repos()
get_teams()




#repo = org.get_repo("testRepo")
#languages = repo.get_languages()
#for l in languages:
#    print l
