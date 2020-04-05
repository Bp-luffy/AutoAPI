#coding=utf-8
from sshtunnel import SSHTunnelForwarder

class sshserver():
    def __init__(self,conf):
        try:
          self.server = SSHTunnelForwarder(
                ssh_address_or_host=(conf['ssh_address_or_host'], conf['ssh_port']),
                ssh_username=conf['ssh_username'],
                ssh_password=conf['ssh_password'],
                remote_bind_address=(conf['remote_bind_address'], conf['port']))
        except Exception as e:
            print('连接ssh异常: %s' % e)

    def start_server(self):
        return self.server.start()

    def close_server(self):
        return self.server.close()

    def get_local_bind_port(self):
        return self.server.local_bind_port


