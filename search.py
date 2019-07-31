import os
import click
import gitlab
import json
import urllib3
from configparser import ConfigParser
from colored import fg, bg, attr

urllib3.disable_warnings()

config = ConfigParser()
cfg_path = os.path.join(os.environ['HOME'], '.gitlab.cfg')
if not os.path.exists(cfg_path):
    cfg_path = '.gitlab.cfg'
config.read(cfg_path)
domain = config['default']['domain']
private_token = config['default']['private_token']

gl = gitlab.Gitlab(domain, private_token=private_token)


def color(text):
    return '{}{} {} {}'.format(fg('white'), bg('yellow'), text, attr('reset'))


def replace(text, word):
    return text.replace(word, color(word))


class Searcher(object):
    def __init__(self, word, count, debug):
        self.word = word
        self.count = count
        self.debug = debug

    def search(self, project):
        results = project.search('blobs', self.word)
        if results:
            print('=' * 10 + project.name + '=' * 10)
            for idx in range(min(self.count, len(results))):
                print(replace(json.dumps(results[idx]), self.word))
        elif self.debug:
            print('=' * 10 + project.name + '=' * 10 + ' None')


def get_all_my_stars():
    stars = []
    projects = gl.projects.list(starred=True, all=True, order_by='name', sort='asc')
    for project in projects:
        stars.append(project.name)
    return stars


@click.command()
@click.option('-w', '--word', help='word to search.')
@click.option('-c', '--count', default=1, help='limit results for each repo.', show_default=True)
@click.option('-s', '--scope', default='all', help='all|star|unstar.', show_default=True)
@click.option('-r', '--repo', help='repo for searching')
@click.option('-f', '--filename', help='file of repo list for searching')
@click.option('--debug/--no-debug', default=False)
def search(word, count, scope, repo, filename, debug):
    print('searching {} on {}...'.format(word, domain))
    if repo:
        projects = [gl.projects.get(repo)]
    elif filename:
        projects = []
        for repo in open(filename, "r").readlines():
            repo_name = repo.strip()
            if repo_name:
                try:
                    project = gl.projects.get(repo_name)
                    projects.append(project)
                except gitlab.exceptions.GitlabGetError:
                    print('=' * 10 + repo_name + '=' * 10 + ' Not exists')
    elif scope == 'star':
        projects = gl.projects.list(as_list=False, starred=True)
    elif scope == 'unstar':
        projects = gl.projects.list(as_list=False)
        stars = get_all_my_stars()
    else:
        projects = gl.projects.list(as_list=False)
    s = Searcher(word, count, debug)
    for project in projects:
        if scope == 'unstar' and project.name in stars:
            continue
        s.search(project)


if __name__ == '__main__':
    search()
