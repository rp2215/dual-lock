
### Models Folder

- defines what each database table looks like using Python classes
- each class maps to a table
- SQLAlchemy will read these classes to undertsand database structure
- then Alembic will read these classes to generate migration scripts for when the schema changes so that we are working on same database structure

### Alembic Use

- when changing one of Python models
- run `alembic revision --autogenerate -m "message"` which generates migration script
- run `alembic upgrade head` which applies the sript to database
- basically works like git but for the database schema