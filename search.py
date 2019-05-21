import os
import click
import gitlab
from configparser import ConfigParser

config = ConfigParser()
cfg_path = os.path.join(os.environ['HOME'], '.gitlab.cfg')
# cfg_path = '.gitlab.cfg'
config.read(cfg_path)
domain = config['default']['domain']
private_token = config['default']['private_token']

gl = gitlab.Gitlab(domain, private_token=private_token)


@click.command()
@click.option('-w', '--word', help='word to search.')
def search(word):
    print('searching {} on {}...'.format(word, domain))
    projects = gl.projects.list(as_list=False)
    for project in projects:
        results = project.search('blobs', word)
        if results:
            print('=' * 10 + project.name + '=' * 10)
            print(results[0])


if __name__ == '__main__':
    search()
