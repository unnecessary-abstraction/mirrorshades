from invoke import task

@task
def install(c):
    """Install the project locally"""
    c.run("pip install .")

@task
def build(c):
    """Build the project"""
    c.run("python3 -m pep517.build .")

@task
def clean(c):
    """Remove build output"""
    c.run("rm -rf build dist src/*.egg-info")
