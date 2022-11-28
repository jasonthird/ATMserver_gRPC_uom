# ATM tellel machine server using gRPC
Exercise for the distributed programming course in university of macedonia

## Python3.10.8 dependences 
mariadb(1.1.4), grpcio(1.50.1), grpcio-tools(1.50.0)
  
## Usage
Given that you have access to a mariadb instance, modify the sqlConfig.json to configure the database connection.
<br>
If you are running it for the first time and need to set the database up just run
``` python3 SqlConnection setupDb```. This will automatically connect to mariadb and create and setup a database (name specified in sqlConfig.json) with some test data.
<br>
<br><br>Run ```python3 server_main.py``` to start the server.

