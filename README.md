# Introduction

Thank you for your interest in Dataframe!

You'll be assigned either the Frontend or Backend project. Please aim to dedicate 4-6 hours on the project, and push your work to a _private_ Github repo.

Some coding guidelines:

- Make commits frequently and do not squash commits when pushing to remote. You should be committing more frequently than you normally would at a job. This will help us see not only the final work product, but also how you think / iterate on your solution.

## Backend project:

Currently, the Documents API provides CRUD operations on the Documents model. When retrieving a list of documents, you can programmatically order it by an attribute such as name, last update date, etc. Your goal is to add manual ordering. From a UX perspective, this will be used by FE engineers to build out a drag-and-drop ordering system where users can drag to reorder documents in a list.

Some technologies you may find useful to reference in completing this project:

- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [Sqlalchemy](https://docs.sqlalchemy.org/en/13/)
- [Postgresql](https://www.postgresql.org/docs/13/index.html)

## Frontend project:

As of now, the FE skeleton read-only text template, but let's build this into a WYSIWYG markdown editor that persists its contents in the API. Build out the application features to support the following requirements:

- State management and API requests are abstracted in MobX stores
- The current document state is persisted to the DB
- User input is saved efficiently wrt network requests
- Display useful feedback info wrt saving: the current saving status + "last updated" timestamp
- BONUS points for additional product- or user-centric improvements!

### Helpful Resources

- [MobX](https://mobx.js.org/README.html#a-quick-example)
- [rich-markdown-editor](https://github.com/outline/rich-markdown-editor)

## Reference

To lift up the api:

```bash
make api
```

To create a new migration file:

```bash
docker ps
docker exec -it 318942bcead9 /bin/bash
cd models/migrations/
alembic revision --autogenerate
```

To lift up the react app:

```bash
make app
```

To run tests:
- ensure `make api` is running
```bash
make test
```