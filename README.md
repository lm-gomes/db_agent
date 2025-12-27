# db_agent
Prototype of an agent capable of interpret definition and manipulation commands into SQL queries. The prototype was first designed for PostgreSQL, but it's functionality can be applied for any SQL based SGBD.

In short terms, instead of giving a specific SQL command, ask the agent using a natural language, and it will translate it to SQL automatically.

For a few tests, the agent acted pretty well, even though I haven't measured the correctiveness with specific metrics.

!ATENTION!
It is not recommended to use this application for critical processes on applications. SQL commands often require a specialist analysis and can break your database logic if not implemented well. The purpose for this project is just for study.


