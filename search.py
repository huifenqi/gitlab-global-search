import os
import click
import gitlab
import json
from configparser import ConfigParser
from colored import fg, bg, attr

import conpig

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
            for idx in range(self.count):
                print(replace(json.dumps(results[idx]), self.word))
        elif self.debug:
            print('=' * 10 + project.name + '=' * 10 + ' None')


@click.command()
@click.option('-w', '--word', help='word to search.')
@click.option('-c', '--count', default=1, help='limit results for each repo.', show_default=True)
@click.option('--debug/--no-debug', default=False)
def search(word, count, debug):
    print('searching {} on {}...'.format(word, domain))
    s = Searcher(word, count, debug)
    projects = gl.projects.list(as_list=False)
    for project in projects:
        # s.search(project)
        conpig.spawn(s.search, project)
    conpig.wait_all()


def get_all_my_stars():
    projects = gl.projects.list(starred=True, all=True, order_by='name', sort='asc')
    for project in projects:
        print(project.web_url)


if __name__ == '__main__':
    search()
    # get_all_my_stars()
