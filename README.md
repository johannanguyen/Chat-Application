1. Clone this repo and install the required dependencies using the following commands:<br>
  a) `git clone https://github.com/johannanguyen/project2-m1-jn354.git`<br>
  b) `npm install`  
  c) `pip install flask-socketio`  
  d) `pip install eventlet`  
  e) `npm install -g webpack`  
  f) `npm install --save-dev webpack`  
  g) `npm install socket.io-client --save`<br>
  If any messages occur, rerun the failed commands but add "sudo " to the beginning of them<br>
      ie. `pip install eventlet` -> `pip install eventlet`
      
2. Get PSQL to work updating yum and pip and installing psycopg2 and SQLAlchemy
by using the following commands:<br>
  a) `sudo yum update` -> answer yes to all prompts<br>
  b) `pip install --upgrade pip`<br>
  c) `pip install psycopg2-binary`<br>
  d) `sudo pip install Flask-SQLAlchemy==2.1`
  
3. Set up PSQL by using the following commands:
  a) Install PostGreSQL<br>
      `sudo yum install postgresql postgresql-server postgresql-devel postgresql-contrib postgresql-docs`<br>
  b) Initialize the PSQL database<br>
      `sudo service postgresql initdb`<br>
  c) Start PSQL<br>
      `sudo service postgresql start`<br>
  d) Make a superuser<br>
      `sudo -u postgres createuser --superuser $USER`<br>
     An error saying "could not change directory" means it worked :)<br>
  e) Make a database<br>
      `sudo -u postgres createdb $USER`<br>
     An error saying "could not change directory" means it worked :)<br>
  f) Make a new user<br>
      `psql`<br>
      `create user [some_username_here] superuser password '[some_unique_new_password_here]';`<br>
     BE SURE TO REPLACE `[some_username_here]` AND `[some_unique_new_password_here]` WITH ACTUAL VALUES<br>
      `\q` to quit out of psql<br>
  g) Create a file called `sql.env` and include the following in that file:<br>
      `export DATABASE_URL='postgresql://[some_username_here]:[some_unique_new_password_here]@localhost/postgres`<br>
     BE SURE TO REPLACE `[some_username_here]` AND `[some_unique_new_password_here]` WITH THE VALUES SET IN 3f<br>
 
4. Enable read/write from SQLAlchemy<br>
  a) Open pg_hba.conf<br>
      `psql`<br>
      `SHOW SHOW hba_file;`<br>
      `sudo vim [location of pg_hba.conf`<br>
  b) Replace all instances of `ident` with `md5`<br>
      `:%s/ident/md5/g`<br>
  c) Replace all instances of `peer` with `md5`<br>
      `:%s/peer/md5/g`<br>
  d) Restart PostGreSQL<br>
      `sudo service postgresql restart`<br>
    
5. Run the program~<br>
  a) `npm run watch`<br>
  b) Open another terminal:<br>
       `python app.py`<br>
  c) Hit `Preview Running Application`<br>
       May need to do a hard refresh by typing `ctrl + shift + r`<br>
     
<b>KNOWN ISSUES</b>
1. The app is not mobile-friendly. Although the functionality remains in tact, the formatting needs some work. The chat box does not resize based on browser size and the background repeats when it is not intended to.

<b>TECHNICAL DIFFICULTIES</b>
1. Replacing the randomly assigned Pokémon name to the user’s actual google login name: This was an issue because initially, I was randomly selecting Pokémon names by pulling information from an API in the backend portion of my project. Realizing that I now had to grab the name information from the client, send it to the server, then back to the client, was more troublesome than I had initially anticipated.
2. Forcing the login page to display before the chatbox: This was difficult to accomplish because I knew that using a hidden `<div>` would work as expected; however, I using using `Paper` from `material-ui` which did not integrate HTML well. After struggling with the login process for some time, I decided to replace my `Paper` styling completely. Making the switch made styling and hiding the chatbox much simpler. 

https://pokemon-chitchat.herokuapp.com/

<img src="https://i.ibb.co/zbGC3vB/p2m2-1.png">
<img src="https://i.ibb.co/SJkvWZ5/p2m2.png">


