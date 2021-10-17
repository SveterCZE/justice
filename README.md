<h1>Introduction</h1>
My first larger project, an application using Pyhon, Flask and SQLite to download open commercial register data from the Czech Ministry of Justice (justice.cz) and convert them into an sqlite3 database. The applicaton also contains a front-end component to search in the database by various properties. The main goal of the application is to provide users with more advanced search options compared to the official search at the Ministry of Justice website. 

<h1>Installation</h1>
Download a zip file containing the whole repository and store it into a folder on your PC. You should preferably use a virtual environment. 

See `requirements.txt` for required packages.

<h1>Running the application</h1>
Firstly, you need to download the open data from the Ministry of Justice and build the database. 

Run `python justice_build.py` which will download all the source files, create an SQLite database and parse the downloaded data into the database. Note that after the downloaded data are uncompressed, they are around 13 GB and the database file has around 3.6 GB. It takes approximately 1 hour to download the data and build the database.

Once the database is built, run `python main.py` and open `http://127.0.0.1:5000` You will be greeted with a search form that is described below.

<h1>Features</h1>
<h2>Search by company properties</h2>
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

<h2>Search by legal persons</h2>
You will be greeted with the following search form:

![image](https://user-images.githubusercontent.com/46304018/116795207-815b5580-aad3-11eb-856a-1fb4e0f9a831.png)

The form allows you to search for legal persons registered in the Commercial Register as members of executive bodies, members of supervisory boards, shareholders in a limited liability companies, sole shareholders in a joint stock companies. The form allows you to search by the following properties:
<ul>
  <li>Company name</li>
  <li>Identification No. (for Czech companies)</li>
  <li>Foreign registration No. (for foreign copmpanies) --- this is yet to be implemented</li>
</ul>  

In the fields where you fill-in input data, you can also select one of the following options:
<ul>
  <li>Your input can be anywere in the result. For example, if you input <i>Trade</i> as a company name, the application will find and return both <i>SILOMAN Trade a.s.</i> and <i>Trade Bridge a.s.</i> </li>
  <li>The result must start with your input. For example, if you input <i>Trade</i> as a company name, the application will find and reutrn only <i>Trade Bridge a.s.</i>, but not <i>SILOMAN Trade a.s.</i></li>
  <li>The result and your input must match. For example, if you input <i>Trade</i> as a company name, the application will neither <i>SILOMAN Trade a.s.</i> nor <i>Trade Bridge a.s.</i></li>
</ul>  

In addition, you can also select whether the application shall return only the legal persons who are still active in the company or whether it shall reutrn also those that are no longer active.

<h2>Display search results</h2>
Once you hit the search button, you the results will be displayed to you. Several examples are displayed below.

A stadard result when you search by company properties.

![image](https://user-images.githubusercontent.com/46304018/116795308-4c9bce00-aad4-11eb-91ee-400e3b3b8813.png)

If a company has an active insolvency record, it will be highlighted in red and the relevant insovlency notes will be added.

![image](https://user-images.githubusercontent.com/46304018/116795388-d8adf580-aad4-11eb-8e34-4db9078a56fc.png)

A standard result when you search for a natural person active in a company. It firstly displays the natural person's identification details and then the identification details of the company in which such person is or was active.

![image](https://user-images.githubusercontent.com/46304018/116795416-11e66580-aad5-11eb-86e0-1cd290f2535d.png)

A standard result when you search for a legal person active in a company. It firstly displays the legal person's identification details and then the identification details of the company in which such person is or was active.

![image](https://user-images.githubusercontent.com/46304018/116795551-2a0ab480-aad6-11eb-98b1-24ea1f9072ed.png)

<h2>Display detailed company data:</h2>
The application also allows you to display detailed data about each company in two forms:

<ul>
<li>Historical extract, showing all data, including those that are no longer relevant</li>
<li>Current extract, showing only the up-to-date data</li>
</ul>

A historical extract can look something like this. The data that are no longer up-to-date are underlined.

![image](https://user-images.githubusercontent.com/46304018/116795933-c930ab80-aad8-11eb-8254-6d6e3a4d751d.png)

A current extract looks like this.
![image](https://user-images.githubusercontent.com/46304018/116795940-d6e63100-aad8-11eb-94d4-2a4841329f56.png)

<h2>Trivia</h2>
You can also explore some interesting information about the data stored in the Commercial register. You can find, for example, a list of the oldest existing companies or addresses at which the most companies have their registered office. Go and check it yourselves :)

<h1>Known issues</h1>
This is an early prototype not yet suitable for production deployment as there are multiple issues that need to be resolved. The main issues are as follows:
<ul>
<li>Czech diacritics are not processed properly and based on my initial research, I suspect that this is due to SQLite limitations.</li>
<li>Not all information available in the open data sets are stored in the application database.</li>  
<li>The underlying code should be refactored to remove excessive duplications.</li>
<li>I should unify the naming of functions and variables. Now, it is a mixtrue of Czech and English language, partly because it uses some Czech legal terms and the same variables that are used in the source open data.</li>  
<li>I should somehow hide the secret keys before deploying the app. I am keeping it in to make it easier for people to test the app.</li>
<li>I do not know how to deploy such application :)</li>

</ul>
