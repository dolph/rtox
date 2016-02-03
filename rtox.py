# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy of
# the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.

import argparse
try:
    import ConfigParser as configparser
except ImportError:
    import configparser
import getpass
import os.path
import sys

import paramiko


class Client(object):
    """An SSH client that can runs remote commands as if they were local."""

    def __init__(self, hostname, port=None, user=None):
        """Initialize an SSH client based on the given configuration."""
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, port=port, username=user)

    def run(self, command):
        """Run the given command remotely over SSH, echoing output locally."""
        channel = self.ssh.get_transport().open_session()
        channel.exec_command(command)
        stdin, stdout, stderr = self.ssh.exec_command(command)

        # Pass remote stdout and stderr to the local terminal
        while not channel.exit_status_ready():
            if channel.recv_ready():
                length = len(channel.in_buffer)
                sys.stdout.write(channel.recv(length))

            if channel.recv_stderr_ready():
                length = len(channel.in_stderr_buffer)
                sys.stderr.write(channel.recv_stderr(length))

        return channel.recv_exit_status()


def load_config():
    """Define and load configuration from a file.

    Configuration is read from ``~/.rtox.cfg``. An example might be::

        [ssh]
        user = root
        hostname = localhost
        port = 22

    SSH passwords are not supported.

    """
    config = configparser.ConfigParser()
    config.add_section('ssh')
    config.set('ssh', 'user', getpass.getuser())
    config.set('ssh', 'hostname', 'localhost')
    config.set('ssh', 'port', '22')
    config.read(os.path.expanduser('~/.rtox.cfg'))
    return config


def cli():
    """Run the command line interface of the program."""
    parser = argparse.ArgumentParser(
        description='Remote tox test runner')
    parser.add_argument('arguments_for_tox', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    config = load_config()

    client = Client(
        config.get('ssh', 'hostname'),
        port=config.getint('ssh', 'port'),
        user=config.get('ssh', 'user'))
    command = [
        'source ~/venv/os/bin/activate os',
        '&&',
        'cd ~/openstack/keystone-specs'
        '&&'
        'tox']
    command.extend(args.arguments_for_tox)
    status_code = client.run(' '.join(command))

    raise SystemExit(status_code)


if __name__ == '__main__':
    cli()
