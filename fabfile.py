# Настройка публикации через fabric
from fabric import task, Connection, Config
from termcolor import colored
from django.utils import timezone
import getpass
import os

# Для django.utils
os.environ['DJANGO_SETTINGS_MODULE'] = 'testing_system.settings'

manager = 'apt'
environment = 'production'
host = '141.144.233.165'  
user = 'ubuntu'

port = 22
path = '/home/apps/testing-system'
git_url = 'https://github.com/maximalekseenko/testing-system.git'

release_dir = timezone.now().strftime("%Y%m%d%H%M%S")
releases_path = f"{path}/releases"
release_path = f"{releases_path}/{release_dir}"
shared_path = f"{path}/shared"
current_path = f"{path}/current"
system_path = f"{shared_path}/system"
log_path = f"{path}/log"
sock_path = f"{path}/sock"

conn = Connection(host, user=user, port=port)


def git_check():
    print(colored('* git check', "blue"))
    conn.run(f"git ls-remote {git_url} HEAD")


def create_release_dirs():
    print(colored('* create release dirs', 'blue'))
    conn.run(f"mkdir -p {releases_path}")
    conn.run(f"mkdir -p {shared_path}")
    conn.run(f"mkdir -p {system_path}")


def create_dirs():
    print(colored('* create dirs', 'blue'))
    conn.sudo(f"mkdir -p {path}")
    conn.sudo(f"chown -R {user} {path}")
    conn.run(f"mkdir -p {sock_path}")
    conn.run(f"mkdir -p {log_path}")


def cleanup():
    print(colored('* cleanup old releases', 'blue'))
    result = conn.run(f"ls -x {releases_path}")
    if not result:
        return
    releases = result.stdout.split()
    if len(releases) <= 5:
        return
    releases.reverse()
    del releases[:5]
    dirs = ' '.join([f"{releases_path}/{directory}" for directory in releases])
    conn.run(f"rm -rf {dirs}")


def create_release():
    print(colored(f"* create release {release_dir}", 'blue'))
    conn.run(f"mkdir -p {release_path}")
    conn.run(f"git clone {git_url} {release_path}")


def link_dirs():
    conn.run(f"ln -nfs {system_path} {release_path}/system")
    conn.run(f"ln -nfs {log_path} {release_path}/log")
    conn.run(f"ln -nfs {shared_path}/.env {release_path}/.env")


def switch_current():
    conn.run(f"ln -nfs {release_path} {current_path}")


def install_requirements():
    print(colored(f"* install requirements", 'blue'))
    conn.run(f"cd {release_path} && pip3 install -r ./requirements.txt --user")


def start_migration():
    print(colored(f"* start migration", 'blue'))
    conn.run(f"cd {release_path} && python3 ./manage.py migrate")


def collect_static():
    print(colored("* collect static files", 'blue'))
    conn.run(f"mkdir -p {release_path}/static")
    conn.run(
        f"cd {release_path} && python3 ./manage.py collectstatic --no-input")


def restart_gunicorn():
    print(colored(f"* restart_gunicorn", 'blue'))
    conn.sudo(f"supervisorctl restart testing-system_gunicorn")


def restart_web():
    print(colored('Restart gunicorn', 'blue'))
    conn.sudo('supervisorctl restart testing-system_gunicorn')
    print(colored('Restart nginx', 'blue'))
    conn.sudo('supervisorctl restart nginx')


@task
def restartweb(context):
    restart_web()


@task
def deploy(context):

    print(colored('Deploy start', 'blue'))
    git_check()
    create_release_dirs()
    create_release()
    link_dirs()
    install_requirements()
    start_migration()
    collect_static()
    switch_current()
    restart_web()
    cleanup()
    print(colored('Deploy complete', 'blue'))
