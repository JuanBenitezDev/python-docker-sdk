import docker
from docker.types import Mount
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_NAME = "sandbox"
OUTPUT_FILE = "output.txt"
CODE_PATH = os.path.join(BASE_DIR, 'code')
DOCKERFILE_PATH = '.'

# Get docker client
client = docker.from_env()

# Build Image
def build_image():
    print('building image')
    image, logs = client.images.build(path=DOCKERFILE_PATH, tag=IMAGE_NAME)
    for log in logs:
        print(log)
    print('finished image')

# Create container
def get_container(cmd):
    mount = Mount(source=CODE_PATH, target='/home/', type='bind',)
    container = client.containers.create(image=IMAGE_NAME, command=cmd, mounts=[mount, ], network_disabled=True, network_mode=None, privileged=False, detach=True,)

    return container

# Delete a container
def delete_container(container):
    container.stop()
    container.remove()

# Build command
def get_command(code):
    """
    params: code is the command used to run the code per language
    """
    command_list = ['/bin/bash', '-c']
    run_cmd = code.split(' ')
    run_cmd.extend(['>>', OUTPUT_FILE])
    cmd_string = ' '.join(run_cmd)
    command_list.append(cmd_string)

    return command_list

# Supported languages
languages = {
    'python': {
        'command': 'python3 code.py'
    },
    'javascript': {
        'command': 'node code.js'
    },
    'golang': {
        'command': 'go run code.go'
    },
    # https://rupinderjeetkaur.wordpress.com/2014/06/20/run-a-cc-program-on-terminal-using-gcc-compiler/
    'c++': {
        'command': 'g++ code.cpp && ./a.out'
    },
    'java': {
        'command': 'java code.java'
    },
    'ruby': {
        'command': 'ruby code.rb'
    },
    'php': {
        'command': 'php code.php'
    }
}

# Run
def run(languages):
    #build_image()
    containers_list = []

    # Create and start containers
    for language in languages:
        cmd = get_command(languages[language]['command'])
        container = get_container(cmd)
        container.start()
        containers_list.append(container)
    # Remove containers
    for container in containers_list:
        delete_container(container)


if __name__ == "__main__":
    run(languages)




