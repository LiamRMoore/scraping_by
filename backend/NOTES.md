It may be useful to map the JSON schema directly to an SQL table.

If the frontend app is interacting with the database through a 
python FastAPI, we will want a pydantic model for the requests.

This could be generated from the json itself by:

https://pydantic-docs.helpmanual.io/datamodel_code_generator/

Then we have to worry about mapping these Pydantic data models 
onto SQL tables.

This is explored in [this issue](https://github.com/tiangolo/fastapi/issues/214).

Tiangolo has a solution which is a WIP: https://github.com/tiangolo/sqlmodel
