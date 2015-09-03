__author__ = 'igor'

from fabric.api import local
import os
from fs.settings import BASE_DIR


def prepare_deploy():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fs.settings")
    activate_env = os.path.expanduser(os.path.join(BASE_DIR, "ENV/bin/activate_this.py"))
    execfile(activate_env, dict(__file__=activate_env))
    # local("./manage.py test")
    local("pip freeze > requirements.txt")
    local("./manage.py collectstatic -c --noinput")
    local("git add .")
    local("git commit -F git_commit_message")
    local("git push origin master")
    local("git push bit")
