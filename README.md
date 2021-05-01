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

The form allows you to search for companies registered in the Commercial Register by the following properties:
<ul>
  <li>Company name</li>
  <li>Identification number</li>
  <li>Municipality</li>
  <li>Street name</li>
  <li>Court register section (<i>oddíl</i>)</li>
  <li>Court register file No. (<i>vložka</i>)</li>
  <li>Legal form</li>
  <li>Court of registration</li>
  <li>Active insolvency record</li>
  <li>Date of registration</li>
</ul>  

In the fields where you fill-in input data, you can also select one of the following options:
<ul>
  <li>Your input can be anywere in the result. For example, if you input <i>Trade</i> as a company name, the application will find and return both <i>SILOMAN Trade a.s.</i> and <i>Trade Bridge a.s.</i> </li>
  <li>The result must start with your input. For example, if you input <i>Trade</i> as a company name, the application will find and reutrn only <i>Trade Bridge a.s.</i>, but not <i>SILOMAN Trade a.s.</i></li>
  <li>The result and your input must match. For example, if you input <i>Trade</i> as a company name, the application will neither <i>SILOMAN Trade a.s.</i> nor <i>Trade Bridge a.s.</i></li>
</ul>  

In addition, you can also select one of the following options:
<ul>
  <li>Your input must match the company data that are up-to-date. For example, if you input <i>Trade</i> as a company name, a company that used to be names <i>Global Trade, a.s.</i>, but had since been renamed, will not be found.</li>
  <li>Your input may match the company data that are no longer up-to-date. For example, if you input <i>Trade</i> as a company name, a company that used to be names <i>Global Trade, a.s.</i>, but had since been renamed, will be found.</li>
</ul>  

<h2>Search by natural persons:</h2>
You will be greeted with the following search form:
![image](https://user-images.githubusercontent.com/46304018/116795147-1dd12800-aad3-11eb-9b83-bbd9cd775090.png)

The form allows you to search for natural persons registered in the Commercial Register as members of executive bodies, members of supervisory boards, prokurists, shareholders in a limited liability companies, sole shareholders in a joint stock companies. The form allows you to search by the following properties:
<ul>
  <li>First name</li>
  <li>Surname</li>
  <li>Date of birth</li>
</ul>  

In the fields where you fill-in input data, you can also select one of the following options:
<ul>
  <li>Your input can be anywere in the result. For example, if you input <i>Nová</i> as a surname, the application will find and return both <i>Novák</i> and <i>Kuhnová</i> </li>
  <li>The result must start with your input. For example, if you input <i>Nová</i> as a surname, the application will find and reutrn only <i>Novák</i>, but not <i>Kuhnová</i></li>
  <li>The result and your input must match. For example, if you input <i>Nová</i> as a surname, the application will neither <i>Novák</i> nor <i>Kuhnová</i></li>
</ul>  

In addition, you can also select whether the application shall return only the persons who are still active in the company or whether it shall reutrn also those that are no longer active.

<h2>Search by natural persons:</h2>

<h2>Trivia:</h2>

<h1>Known issues:</h1>

