import nox
from nox.sessions import Session


@nox.session(reuse_venv=True)
def format_code(session: Session):
    session.install("isort", "-U")
    session.install("black", "-U")

    session.run("isort", "ottbot")
    session.run("black", "ottbot")
