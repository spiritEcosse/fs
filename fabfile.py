__author__ = 'igor'

from fabric.api import local, run, require, cd
import os
from fs.settings import BASE_DIR
from fabric.state import env
env.hosts = ['root@78.24.216.187']
env.user = 'root'
PROJECT_DIR = '/home/igor/web/www/fs/'
REQUIREMENTS_FILE = 'requirements.txt'
TORNADO_SCRIPT = 'tornado_main.py'


def prepare_deploy():
    local_act()
    update_requirements()
    touch()


def local_act():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fs.settings")
    activate_env = os.path.expanduser(os.path.join(BASE_DIR, "ENV/bin/activate_this.py"))
    execfile(activate_env, dict(__file__=activate_env))
    local("./manage.py test")
    local("%s%s" % ('pip freeze > ', REQUIREMENTS_FILE))
    local("./manage.py collectstatic -c --noinput")
    local("git add .")
    local("git commit -F git_commit_message")
    local("git push origin")
    local("git push bit")


def touch():
    run('touch %s' % TORNADO_SCRIPT)


def update_requirements():
    """ update external dependencies on remote host """
    with cd(PROJECT_DIR):
        run('source ENV/bin/activate')
        run('%s%s' % ('pip install -r ', REQUIREMENTS_FILE))

    # require('code_root', provided_by=('staging', 'production'))
    # requirements = os.path.join(env.code_root, 'requirements')
    # with cd(requirements):
    #     cmd = ['pip install']
    #     cmd += ['-E %(virtualenv_root)s' % env]
    #     cmd += ['--requirement %s' % os.path.join(requirements, 'requirements.txt')]
    #     run(' '.join(cmd))
