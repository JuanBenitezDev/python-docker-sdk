import docker
import json

client = docker.from_env()

# Run a container
msg = client.containers.run("ubuntu", "echo hello world")
client.containers.run()
print(msg)

# Run container in background
container = client.containers.run("bfirsh/reticulate-splines", detach=True)

print(container)

# Get list of containers
containers = client.containers.list()

for container in containers:
    if container.attrs['Config']['Image'] == "bfirsh/reticulate-splines":
        # Get all attributes
        #print(json.dumps(container.attrs, indent=4))
        # Stop a container
        container.stop()

# Get all images
images = client.images.list()

for image in images:
    print(image)