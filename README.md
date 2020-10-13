1. Clone this repo and install the required dependencies using the following commands:<br>
  a) `git clone https://github.com/johannanguyen/project2-m1-jn354.git`<br>
  b) `npm install`  
  c) `pip install flask-socketio`  
  d) `pip install eventlet`  
  e) `npm install -g webpack`  
  f) `npm install --save-dev webpack`  
  g) `npm install socket.io-client --save`  
  h) `npm install @material-ui/core`<br>
  If any messages occur, rerun the failed commands but add "sudo " to the beginning of them<br>
      ie. `npm install @material-ui/core` -> `sudo npm install @material-ui/core`
      
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
1. The code is piled up on top of each other and needs to be refactored. Although this does not hinder its performance, it dampens the code's organization and readability.<br>
2. As the number of messages increase, the time it takes to send greatly increases. I would like to combat this by implementing a "slow" chat-mode, forcing people to only send messages once every ~ 2 seconds.<br>
3. Usernames are assigned by randomly selecting one out of 300 names. In this case, there is a possibility that two users may have the same username at the same time.

<b>TECHNICAL DIFFICULTIES</b>
1. Displaying both the message and the username who sent the message: I realized that passing the information through the sockets as a dictionary made it much easier to parse and therefore easier to display both values on the screen concurrently.<br>
2. Displaying the number of users: My original idea of updating the user count every time a user connected or disconnected did not go as planned. Although most of the clients were seeing the correct number of users, the most-recently connected client would continue to see "0". I fixed this by sending the user count, along with a random username, to each specific user as they entered the chat (using request.sid). This way, as soon as somebody entered, they would be notified of how many users are currently participating in the chat.<br>
3. Printing the entire chat history when a new user started using the application: Initially, my application was displaying one long string of concatenated usernames and another long string of concatenated messages. I added another useEffect to my program to handle prior messages. When mapping across all the prior messages, I used the map's "index" member to match the message with the corresponding sender. Once this map was printed, I continued to map through all the new messages that were being sent.<br>
4. Deployment: Deploying to Heroku was riddled with troubles. I constantly received the error where "refs could not be specified", so I had to remove the git remote and re-add it with the proper github repo link. I then ran into the error of not having proper authentication, so I had to add another ssh key via `heroku keys:add ~/.ssh/id_rsa.pub`. Another error occurred relating to "Peer Authentication Failed," where I had to alter the `pg_hba.conf` a bit more and replace `peer` with `mp5`. This was tedious because I didn't have the proper permissions to view each parent directory which led to where the file was located, so I had to `sudo chmod 777 [name] ` all of them to get to the proper location.
