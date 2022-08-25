# Service-Project

its teh service project...

## Contributing

Python 3.10+

```bash
python -m venv .venv
. .venv/bin/activate
pip install pip -U
pip install -r requirements.txt -r dev-requirements.txt -U

alembic upgrade head

uvicorn api.main:app --reload --port 8080
```

## TODO

- [ ] fix sqlite complaining about thread safety => move to postgres <https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app>
- [ ] add real opportunity models
- [ ] fix absolute imports not working (if there is more than 1 file)
- [ ] add auto migrations <https://alembic.sqlalchemy.org/en/latest/autogenerate.html>
