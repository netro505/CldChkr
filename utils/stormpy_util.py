from utils.docker_util import DockerUtil
import tarfile
import os

class StormpyUtil:
    def __init__(self):
        self.stormpy_docker = DockerUtil("stormpy", "/opt/stormpy")
    
    def add_to_tar_file(self, tarfile_path, files):
        tar = tarfile.open(tarfile_path, mode='w')
        for file_ in files:
            file_name = os.path.basename(file_)
            print(file_name)
            tar.add(file_, arcname=file_name)
        tar.close()
    
    def list_full_paths(self, directory):
        return [os.path.join(directory, file) for file in os.listdir(directory)]
    
    def copy_stormpy_driver_to_docker(self):
        stormpy_driver_tar_path = os.path.abspath("./docker/stormpy-driver.tar")
        stormpy_driver_files_path = os.path.abspath("./stormpydriver")
        stormpy_driver_files = self.list_full_paths(stormpy_driver_files_path)
        self.add_to_tar_file(stormpy_driver_tar_path, stormpy_driver_files)
        self.stormpy_docker.copy_tar_to_container(stormpy_driver_tar_path)  

    def copy_input_files_to_docker(self, input_files):
        input_files_tar_path = os.path.abspath("./docker/input-files.tar")
        self.add_to_tar_file(input_files_tar_path, input_files)
        self.stormpy_docker.copy_tar_to_container(input_files_tar_path)  
    
    def check_model3(self, input_files):
        self.copy_input_files_to_docker(input_files)
        output = DockerUtil.get_container_command_execution("stormpy-test7.py")
        return output

    def get_model_info(self, input_files):
        self.copy_input_files_to_docker(input_files)
        output = self.stormpy_docker.get_container_command_execution("stormpy_model_info.py")
        return output

    def verify_model(self, input_files):
        self.copy_input_files_to_docker(input_files)
        output = self.stormpy_docker.get_container_command_execution("stormpy_verify_model.py")
        return output