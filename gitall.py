import os
import subprocess
import click
import gitlab
import urllib3
from configparser import ConfigParser

urllib3.disable_warnings()

config = ConfigParser()
cfg_path = os.path.join(os.environ['HOME'], '.gitlab.cfg')
if not os.path.exists(cfg_path):
    cfg_path = '.gitlab.cfg'
config.read(cfg_path)
domain = config['default']['domain']
private_token = config['default']['private_token']

gl = gitlab.Gitlab(domain, private_token=private_token)


@click.command()
@click.option('-u', '--user', help='user/organization to get.')
@click.option('-o', '--output', help='output path to store.', default=os.path.curdir, show_default=True)
@click.option('--debug/--no-debug', default=False, show_default=True)
def search(user, output, debug):
    print('get all repos of {} on {}...'.format(user, domain))
    projects = gl.projects.list(as_list=False)
    progress = 0
    repo_count = len(projects)
    for project in projects:
        repo_name = project.name
        progress += 1
        if os.path.exists(os.path.join(output, repo_name)):
            action = 'skipping...'
        else:
            git_url = 'git clone --depth 1 git@git.hzfapi.com:huifenqi/{}.git'.format(repo_name)
            subprocess.call(git_url, cwd=output, shell=True)
            action = 'processed.'
        print('Progress: {}/{} {} {}'.format(progress, repo_count, repo_name, action))


if __name__ == '__main__':
    search()
