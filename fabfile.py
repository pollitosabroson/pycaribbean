# -*- coding: utf-8 -*-
from fabric.api import cd, env, require, run, task
from fabric.colors import green, white
from fabric.context_managers import contextmanager, shell_env
from fabric.utils import puts

from fabutils import arguments, join, options
from fabutils.env import set_env_from_json_file
from fabutils.context import cmd_msg
from fabutils.tasks import ulocal, urun, ursync_project
from fabutils.text import SUCCESS_ART


@contextmanager
def virtualenv():
    """
    Activates the virtualenv in which the commands shall be run.
    """
    require('site_dir', 'django_settings')

    with cd(env.site_dir):
        with shell_env(DJANGO_SETTINGS_MODULE=env.django_settings):
            yield


@task
def environment(env_name):
    """
    Creates a dynamic environment based on the contents of the given
    environments_file.
    """
    if env_name == 'vagrant':
        result = ulocal('vagrant ssh-config | grep IdentityFile', capture=True)
        env.key_filename = result.split()[1].replace('"', '')

    set_env_from_json_file('environments.json', env_name)


@task
def createdb():
    """
    Creates a new database instance with utf-8 encoding for the project.
    """
    urun('createdb pycaribbean -l en_US.UTF-8 -E UTF8 -T template0')


@task
def resetdb():
    """
    Reset the project's database by dropping an creating it again.
    """
    urun('dropdb pycaribbean')
    createdb()
    migrate()


@task
def bootstrap():
    """
    Builds the environment to start the project.
    """
    # Build the DB schema and collect the static files.
    createdb()
    migrate()
    collectstatic()


@task
def loaddata(*args):
    """
    Loads the given data fixtures into the project's database.
    """
    with virtualenv():
        run(join('python manage.py loaddata', arguments(*args)))


@task
def makemigrations(*args, **kwargs):
    """
    Creates the new migrations based on the project's models changes.
    """
    with virtualenv():
        run(join('python manage.py makemigrations',
                 options(**kwargs), arguments(*args)))


@task
def migrate(*args, **kwargs):
    """
    Syncs the DB and applies the available migrations.
    """
    with virtualenv():
        run(join('python manage.py migrate',
                 options(**kwargs), arguments(*args)))


@task
def collectstatic():
    """
    Collects the static files.
    """
    with virtualenv():
        run('python manage.py collectstatic --noinput')


@task
def runserver():
    """
    Starts the development server inside the Vagrant VM.
    """
    with virtualenv():
        run('python manage.py runserver_plus 0.0.0.0:8000')


@task
def deploy(git_ref, upgrade=False):
    """
    Deploy the code of the given git reference to the previously selected
    environment.
    Pass ``upgrade=True`` to upgrade the versions of the already installed
    project requirements (with pip).
    """
    require('hosts', 'user', 'group', 'site_dir', 'django_settings')

    # Retrives git reference metadata and creates a temp directory with the
    # contents resulting of applying a ``git archive`` command.
    message = white('Creating git archive from {0}'.format(git_ref), bold=True)
    with cmd_msg(message):
        repo = ulocal(
            'basename `git rev-parse --show-toplevel`', capture=True)
        commit = ulocal(
            'git rev-parse --short {0}'.format(git_ref), capture=True)
        branch = ulocal(
            'git rev-parse --abbrev-ref HEAD', capture=True)

        tmp_dir = '/tmp/blob-{0}-{1}/'.format(repo, commit)

        ulocal('rm -fr {0}'.format(tmp_dir))
        ulocal('mkdir {0}'.format(tmp_dir))
        ulocal('git archive {0} ./src | tar -xC {1} --strip 1'.format(
            commit, tmp_dir))

    # Uploads the code of the temp directory to the host with rsync telling
    # that it must delete old files in the server, upload deltas by checking
    # file checksums recursivelly in a zipped way; changing the file
    # permissions to allow read, write and execution to the owner, read and
    # execution to the group and no permissions for any other user.
    with cmd_msg(white('Uploading code to server...', bold=True)):
        ursync_project(
            local_dir=tmp_dir,
            remote_dir=env.site_dir,
            delete=True,
            default_opts='-chrtvzP',
            extra_opts='--chmod=750',
            exclude=["*.pyc", "env/", "cover/"]
        )

    # Performs the deployment task, i.e. Install/upgrade project
    # requirements, syncronize and migrate the database changes, collect
    # static files, reload the webserver, etc.
    message = white('Running deployment tasks', bold=True)
    with cmd_msg(message, grouped=True):
        with virtualenv():

            message = white('Installing Python requirements with pip')
            with cmd_msg(message, spaces=2):
                run('pip install -{0}r ./requirements/production.txt'.format(
                    'U' if upgrade else ''))

            message = white('Migrating database')
            with cmd_msg(message, spaces=2):
                run('python manage.py migrate --noinput')

            message = white('Collecting static files')
            with cmd_msg(message, spaces=2):
                run('python manage.py collectstatic --noinput')

            message = white('Setting file permissions')
            with cmd_msg(message, spaces=2):
                run('chgrp -R {0} .'.format(env.group))
                run('chgrp -R {0} ../media'.format(env.group))

            message = white('Restarting webserver')
            with cmd_msg(message, spaces=2):
                run('touch ../reload')

            message = white('Registering deployment')
            with cmd_msg(message, spaces=2):
                register_deployment(commit, branch)

    # Clean the temporary snapshot files that was just deployed to the host
    message = white('Cleaning up...', bold=True)
    with cmd_msg(message):
        ulocal('rm -fr {0}'.format(tmp_dir))

    puts(green(SUCCESS_ART), show_prefix=False)
    puts(white('Code from {0} was succesfully deployed to host {1}'.format(
        git_ref, ', '.join(env.hosts)), bold=True), show_prefix=False)


@task
def register_deployment(commit, branch):
    """
    Register the current deployment at Opbeat with given commit and branch.
    """
    with virtualenv():
        run(
            'opbeat -o $OPBEAT_ORGANIZATION_ID '
            '-a $OPBEAT_APP_ID '
            '-t $OPBEAT_SECRET_TOKEN deployment '
            '--component path:. vcs:git rev:%s branch:%s '
            % (commit, branch)
        )
