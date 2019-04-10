# SOEN487_Project
Private Repo for SOEN 487 Web Services Class Written in Flask

## How-to
- Install dependencies for each server
  - `pip install -r requirements.txt`
- run `main.py` in each application in order:
  1. Authentication Server
  2. Resource Server
  3. Application Server
  
 ## Server URLs
 Authenication  `http://127.0.0.1:9000/` <br/>
 Resource       `http://127.0.0.1:5000/` <br/>
 Application    `http://127.0.0.1:8000/` <br/>
 
 ## Notes
 - can change the server passwords in `/AuthenticationServer/config.py`
 - keep server options in config file
 - each server should have `getAuthToken()` which runs at server initialization (in `main.py`)

 ## TODO:
- check/use cache server response
- remove temp fix on resource server sending all data
- add auth to resource/cache server
- add forwarded token authorization -ie check source request token at auth server
- add tests
- format HTML output of information 
