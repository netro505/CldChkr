import docker
import sys
class DockerUtil:
    def __init__(self, container_name, container_path):
        self.container_name = container_name
        self.container_path = container_path
        self.client = None
        self.container = None
        self.container_status = None
        self.instantiate_docker_client()
    
    def instantiate_docker_client(self):
        try:
            self.client = docker.from_env() # instantiate a client
            self.get_container()
            
            self.container_status = self.container.attrs['State']['Status']
            
            if self.container_status != "running":
                self.container.start()
            
            return self.client
        except Exception as e:
            print(e)
            print(f"Problem with {self.container_name} at {self.container_path}")
            sys.exit(1)
            
    def get_container(self):
        try:
            self.container = self.client.containers.get(self.container_name)
            return self.container
        except Exception as e:
            print(e)
            sys.exit(1)

    def get_container_command_execution(self, stormpy_driver):
        result = self.container.exec_run(f'python {stormpy_driver}')
        return result.output.decode()        
            
    def copy_tar_to_container(self, tarfile_path):
        with open(tarfile_path, 'rb') as f:
            data = f.read()
            self.client.api.put_archive(self.container_name, self.container_path, data)