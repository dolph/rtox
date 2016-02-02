import argparse
import os
import sys

import paramiko


class Client(object):
    def __init__(self, hostname, port=None, user=None, password=None):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname, port=port, username=user, password=password)

    def cmd(self, command):
        channel = self.ssh.get_transport().open_session()
        channel.exec_command(command)
        stdin, stdout, stderr = self.ssh.exec_command(command)

        # Pass remote stdout and stderr to the local terminal
        while not channel.exit_status_ready():
            if channel.recv_ready():
                sys.stdout.write(channel.recv(1))

            if channel.recv_stderr_ready():
                sys.stderr.write(channel.recv_stderr(1))

        return channel.recv_exit_status()


def main():
    parser = argparse.ArgumentParser(
        description='Remote tox test runner')

    parser.add_argument(
        '--ssh-hostname',
        default=os.environ.get('RTOX_SSH_HOSTNAME'))
    parser.add_argument(
        '--ssh-user',
        default=os.environ.get('RTOX_SSH_USER'))
    parser.add_argument(
        '--ssh-port', type=int,
        default=os.environ.get('RTOX_SSH_PORT'))

    args = parser.parse_args()

    client = Client(args.ssh_hostname, port=args.ssh_port)
    command = [
        'source ~/venv/os/bin/activate os',
        '&&',
        'cd ~/openstack/keystone-specs && tox']
    status_code = client.cmd(' '.join(command))

    raise SystemExit(status_code)


if __name__ == '__main__':
    main()
