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

### Create a Migration

```bash
alembic revision --autogenerate -m "add/update ..."

# make sure the migration was generated properly
nvim ./alembic/versions/<revision>.py

alembic upgrade head
```

## SQLAlchemy Docs

<https://docs.sqlalchemy.org/en/14/orm/queryguide.html>
<https://docs.sqlalchemy.org/en/14/tutorial/orm_data_manipulation.html>

## TODO

- [ ] get, create, update, delete users
- [ ] get, create, update, delete tags
- [ ] add tag to user, delete tag if no user has it

- [ ] add real opportunity models
- [ ] handle database errors better <https://fastapi.tiangolo.com/tutorial/handling-errors/>

- [ ] refactor file if it gets too large
  - [ ] main.py
  - [ ] schemas.py
  - [ ] models.py
  - [ ] routers
  - [ ] db.py

- [x] fix sqlite complaining about thread safety => move to postgres <https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app>
- [x] fix absolute imports not working (if there is more than 1 file)
- [x] add auto migrations <https://alembic.sqlalchemy.org/en/latest/autogenerate.html>
- [x] edit and delete routes
- [x] status codes
- [x] add user table and create relations (many to many)
