import subprocess

class DockerBuilder:
    def __init__(self, dockerfile_path):
        self.dockerfile_path = dockerfile_path
    
    def clone_repo(self, repo_url):
        # Clone the repository using git
        subprocess.run(['git', 'clone', repo_url])
    
    def build_docker_image(self):
        # Build the Docker image using the Dockerfile
        subprocess.run(['docker', 'build', '-t', 'my-image', self.dockerfile_path])

# Usage
builder = DockerBuilder('./Dockerfile')
builder.clone_repo('https://github.com/user/repo.git')
builder.build_docker_image()