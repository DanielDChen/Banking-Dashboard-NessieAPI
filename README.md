# API Demo App for Harvard HCS Bootcamp

A simple banking dashboard that shows a user's accounts and transfers, and allows a user to create a transfer. This app uses Capital One's Nessie API for all data, in a Python Flask application.

## Requirements  

* Python 2.7
* Pip for the appropriate version of Python (https://pip.pypa.io/en/stable/installing/)

## Installation

1. Clone the project.

	```
	git clone https://github.com/nessieisreal/api-demo-starter.git
	```  

2. Navigate to the root of the project and create a file `config.py`.

3. Open the file you just created (config.py) and add your Nessie API key as a variable.  
	
	```
	API_KEY = "my_api_key"
	```  

	Retrieve your API key by creating an account at http://api.reimaginebanking.com.

4. Install required packages.
	
	```
	pip install -r requirements.txt
	```  
	
If you run into errors with this command, try upgrading Pip.  

* Mac  
    ```
    pip install -U pip
    ```  
* Windows  
    ```
    python -m pip install -U pip
    ```  
Also, using `sudo` in front of these commands may solve some issues. 

## Running the Application

Navigate to the root of the project and run:

```
python run.py
```  
	
Navigate to **localhost:5000** to view the dashboard.

