import os
import click
import gitlab
import json
from configparser import ConfigParser
from colored import fg, bg, attr

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


@click.command()
@click.option('-w', '--word', help='word to search.')
@click.option('-c', '--count', default=1, help='limit results for each repo.', show_default=True)
@click.option('--debug/--no-debug', default=False)
def search(word, count, debug):
    print('searching {} on {}...'.format(word, domain))
    projects = gl.projects.list(as_list=False)
    for project in projects:
        results = project.search('blobs', word)
        if results:
            print('=' * 10 + project.name + '=' * 10)
            for idx in range(count):
                print(replace(json.dumps(results[idx]), word))
        elif debug:
            print('=' * 10 + project.name + '=' * 10 + ' None')


if __name__ == '__main__':
    search()
