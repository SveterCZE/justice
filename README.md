# justice
<h1>Introduction:</h1>
My first larger project, an application using Pyhon, Flask and SQLite to download open commercial register data from the Czech Ministry of Justice (justice.cz) and convert them into an sqlite3 database. The applicaton also contains a front-end component to search in the database by various properties. 

<h1>Installation:</h1>

<h1>Running the application:</h1>
Firstly, you need to download the open data from the Ministry of Justice and build the database. Run "python justice_build.py", which will download all the source files, create an SQLite database and parse the downloaded data into the database. Note that after the downloaded data are uncompressed, they are around 13 GB and the database file has around 3.6 GB. It takes approximately 1 hour to download the data and build the database.

Once the database is built, run "python main.py".

Features:

Known issues:
