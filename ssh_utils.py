import paramiko


class SSHConnection:
    def __init__(self, ip, port, user, password):
        self.ip = ip
        self.port = port
        self.user = user
        self.password = password
        self.client = None

    def connect(self):
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.ip,
                port=self.port,
                username=self.user,
                password=self.password,
            )
            return True
        except Exception as e:
            print(f"Error conectando a {self.ip}:{self.port} -> {e}")
            return False

    def exec_command(self, command):
        if not self.client:
            raise Exception("No hay conexión SSH activa")
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()

    def close(self):
        if self.client:
            self.client.close()