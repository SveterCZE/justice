# justice
<h1>Introduction:</h1>
My first larger project, an application using Pyhon, Flask and SQLite to download open commercial register data from the Czech Ministry of Justice (justice.cz) and convert them into an sqlite3 database. The applicaton also contains a front-end component to search in the database by various properties. The main goal of the application is to provide users with more advanced search options compared to the official search at the Ministry of Justice website. 

<h1>Installation:</h1>

<h1>Running the application:</h1>
Firstly, you need to download the open data from the Ministry of Justice and build the database. Run "python justice_build.py", which will download all the source files, create an SQLite database and parse the downloaded data into the database. Note that after the downloaded data are uncompressed, they are around 13 GB and the database file has around 3.6 GB. It takes approximately 1 hour to download the data and build the database.

Once the database is built, run "python main.py" and open http://127.0.0.1:5000 You will be greeted with a search form that is described below.

<h1>Features:</h1>
<h2>Search by company properties:</h2>
You will be greeted with the following search form.

![image](https://user-images.githubusercontent.com/46304018/116794252-e90da280-aacb-11eb-92aa-93cb300c2043.png)

The form allows you to search by the following properties:
<list>
  <ul>Company name</ul>
  <ul>Identification number</ul>
  <ul>Municipality</ul>
  <ul>Street name</ul>
  <ul>Court register section (<i>oddíl</i>)</ul>
  <ul>Court register file No. (<i>vložka</i>)</ul>
  <ul>Legal form</ul>
  <ul>Court of registration</ul>
  <ul>Active insolvency record</ul>
  <ul>Date of registration</ul>
</list>  
  
<h2>Search by natural persons:</h2>

<h2>Search by natural persons:</h2>

<h2>Trivia:</h2>

<h1>Known issues:</h1>

