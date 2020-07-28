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

@task
def release(c, version):
    """Release a version of the project"""
    clean(c)
    c.run(f"sed -i 's/^\(__version__ =\).*$/\\1 \"{version}\"/' src/mirrorshades/__init__.py")
    c.run(f"git commit -s -m 'Release {version}' src/mirrorshades/__init__.py")
    build(c)
    c.run(f"echo mirrorshades {version} > dist/RELEASE_NOTES.txt")
    c.run(f"markdown-extract -fri '^{version}' ChangeLog.md >> dist/RELEASE_NOTES.txt")
    c.run(f"git tag -a -F dist/RELEASE_NOTES.txt 'v{version}' HEAD")
    with c.cd("dist"):
        c.run("sha256sum * > SHA256SUMS")
