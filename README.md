JAMDO
## Overview

Our web application leverages information retrieval returning engaging and compelling information based on the date of an event, more specifically historical events, deaths or births. Given the date the application will search and return a wide variety of relevant information to display to the user. A web crawler will be required to search and gather for information based on user inputs. This will entail utilizing existing 3rd party APIs as an efficient way of retrieving specific data. To optimize the web crawling, reduce requests, and lower wait times, previously searched information will be saved in persistent data. The managing of persistent data will require the creation of a caching engine to detect, return, and update data in the databases. Finally aside from a users'' ability to query data, asynchronous requests will be made to give users an \'infinite scroll\'. Here JAMDO makes background requests to the server for additional dates of information. The application will utilize four microservices to manage the resources and data it collects; the main application user service, resource gathering of relevant information, data caching of previously requested information, and continuous asynchronous requests.

### Features
- Use of external 3rd Party Apis
- Parsing of Wiki API response
- Cross Server RESTful API
- User and Server Authentication with JWT
- Encryption with BCrypt
- Implementation of caching system
- Asynchronous requests
- Decorators

### Technical Microservice Description:
The following table represents the public API endpoints. Listed are both the URI which browsers will use and the application will hyperlink returning a HTML document. All microservice servers, aside from the application server, will both respond to and return JSON data. For the following tables of endpoints, paths are relative to the set application host (*127.0.0.1*). Each server, if not running individually on their own devices, are identified by these localhost ports:

| Server         | Port |
|----------------|------|
| Application     | 7000 |
| Resource       | 3000 |
| Caching        | 5000 |
| Authentication | 9000 |

#### 1. Resource Gathering Server
This microservice responds to HTTP requests describing a date in the format YYYY-MM-DD. Given these parameters predetermined 3rd party APIs will be queried to generate a list of interesting information. The current build of JAMDO utilizes *Media wiki API* to query for notable births, deaths, and events. After finding the relevant Wiki page with the aid of the wiki API, Resource Gathering uses its own parser to get the relevant information..

| Methods              | HTTP   Request       |  Response    |          Description                  |
|----------------------|----------------------|-----------------------------------------|----|
| return_event_day     | GET /event_type/year/month/day  |  200 JSON | Return all information on that day from wiki in json format  |
| return_event_month   | GET /event_type/year/month/ | 200 JSON | Return all information on that month from wiki in json format |
| return_event_year    | GET /event_type/year/    |  200 JSON |Return all information on that year from wiki in json format     |

Example: Getting the event_type information for a specific day<br />

Method : return_event_day<br />
  Route : /event_type/year/month/day<br />
  Event_type:  can be “event”, “birth” or “death” <br />
  Event : historical event(s) that happened that date <br />
  Birth : birth(s) that happened that date <br />
  Death : deaths(s) that happened that date <br />
  Example input : /birth/1948/1/2 
  

#### 2. Data Persistence/Caching Server
The Caching Server describes the state of the persistent data retrieved from the Resource Server. Dates not present in the database are expected to be populated by the Resource Server.

| Request | Response                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /:Year/:Month/:Day         | 200 JSON                  | Query of data in database                 |
| POST (**Authenticated**)        | 200 JSON, POST -> Application Server          |Response of successful data store, Signals newly saved|

#### 3. Authentication Server
This server verifies that certain requests are made by Application microservices. Authenticated requests will produce specific functions from the server. When each other servers start and initializes, it sends a request with its name and server password. This registers the server with the Authentication Server and is given a token and, the Authentication Server saving a copy in its database. The token should persist in each servers’ working memory and forward it to the other microservices when making requests. The responding server will forward the cookie to the Authentication Server to validate and will continue the transaction if the authentication approves.

| Request | Reponse                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /getToken/        | 200 JSON                  | Gives microservice server unique token                 |
| GET /authenticate/        | 200 JSON          |Validates service ID from token|

#### 4. Asynchronous Requests
This front-end microservice detects user interactions and creates background requests to continuously generate content for Client. Once loaded, a script detects the visible window position and, when at the end of the page, makes a new request to the application server to get a random row from the Cache Server. The returned JSON data is specially formatted and presented to clients.

#### 5. Application Server
The hub that connects the user interface to the the other microservices. This server acts as the clients’ endpoint being given the outcome of the requests and responses from the various other services. The application server also manages users, allowing them to register and log in. The server expects HTTP arguments as inputs and outputs HTML. The only supported RESTful API is the */getRandom* endpoint which is used by the asynchronous requests.

| Request | Response                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /            | 200 HTML | Returns
| POST /           | 200 HTML | JSON 3rd API data (from Resource or Cache Server) applied to template view for client|
| GET /getRandom/        | 200 JSON    | Requests a random row from the Caching Server database    |
| GET /login/        | 200 HTML  |User logs into JAMDO    |
| GET /register/        | 200 HTML |Client registration into JAMDO    |

## Sample Use Case
This traces the path taken from the user request of a date to the output of a date to the HTML output of the structured gathered resource.

1. Front-end request of 1989/01/23
2. Application server query of Caching Server for 1989/01/23
3. Cache Server requests authentication of Application Server
4. Authentication Server verifies Application Server
5. Cache Server queries local database for date 1989/01/23
6. Cache Server response of query (assume cache miss) to Application Server
7. Application Server request for 1989/01/23 from Resource Server
8. Resource Server requests authentication of Application Server
9. Authentication Server verifies Resource Server
10. Gathering/Processing of data from 3rd party APIs
11. Resource Server POST request of newly processed data to Cache Server
12. Cache Server requests authentication of Resource Server
13. Authentication Server verifies Resource Server
14. Resource Server response of processed JSON data to Application Server
15. Processing of response JSON to application view template
16. HTML Response to Client

### Deployment
JAMDO was alpha tested on the Heroku PaaS and later updated to the build to be submitted for the submission. Each server was given its own *dyno*, a single process instance in their service where the host is the subdomain given to the application. 

| Server         | domain                                  |
|----------------|-----------------------------------------|
| Application     | jamdo-487.herokuapp.com                 |
| Resource       | resource-server-487.herokuapp.com       |
| Caching        | cache-server-487.herokuapp.com          |
| Authentication | authentication-server-487.herokuapp.com |

Heroku limits the bandwidth and *sleeps* the application if not in use for more than 30 minutes. This causes the app as a whole to feel unresponsive at its first request after sleeping. There may also be errors if the Application Server is not active when the others attempt to register/authenticate.

Specific changes were made to each microservice to be deployed to Heroku. Firstly, all localhost addresses and ports were changed to the subdomain registered with Heroku. Next, a linux based HTTP server *gunicorn* module was added to the requirements.txt of all servers. This is a specific module required to run the Flask application on the Heroku servers. Finally, a Procfile was added to the root of the server directory to instruct the platform to execute gunicorn and run the application from main.py

Errors may occur when registering a username that already exists or logging with an non existing account, this however does not occur in the local version. As message flashing was not included in the deployed version.

https://jamdo-487.herokuapp.com 

## Known issues and bugs:
- Cache system does not consider stale Wiki information in database
- Caching hits not being detected
- Some dates do not return any information
- There is no information for Years before 1900 and after 2018
- There is no information for births after 2001
- Returned information formatting can be messy
- Front-end async makes too many uncontrolled requests
- Async can return duplicate instances from the database
## Improvements:

To improve the application and increase the robustness these are proposed features to improve JAMDO.
- More types of resources to gather, more 3rd party APIs
- Customized user content based on searches
- RESTful API for base application, not just microservices
- API key generator for client use of JAMDO microservices

## Resources
https://gsa.github.io/api-documentation-template/api-docs/ 

http://flask.pocoo.org/docs/1.0/api/ 

https://2.python-requests.org/en/master/ 

https://docs.sqlalchemy.org/en/13/ 

https://mwparserfromhell.readthedocs.io/en/latest/ 

https://pyjwt.readthedocs.io/en/latest/index.html 

https://github.com/pyca/bcrypt/ 

http://jinja.pocoo.org/docs/2.10/

https://devcenter.heroku.com/articles/getting-started-with-python

## Installation Instructions:
Each server exists in its own directory with the required dependencies and modules existing in *requirements.txt*. 
To start any server, main.py contains the run protocol. The entire application requires that the authentication server starts before the others as they request registration to gain an authentication token. 

Go into each individual folder and type python main.py in the git bash command line or in the command prompt assuming python exists in the environment settings.

## Contributors:
- James Edwards, jamese1394, jamesedwards1394@gmail.com
- Andy Nguyen, asianswagstorm, nguyen.andy123@gmail.com
- Manuel Toca, mtoca, manueltoca03@gmail.com
- Nguyen Dinh, Dinher, ngd253@mail.usask.ca
- Olivier Mercier Peetz, kothve, oliviermercierpeetz@live.ca
## Tasks breakdown and responsibilities:
- James Edwards: Caching server, Testing, Presentation
- Andy Nguyen: User Login/Registration, Application Server, Testing, Presentation
- Manuel Toca: Caching server, Testing, Presentation
- Nguyen Dinh: Authentication server, Application Server, Testing, Presentation, Deployment
- Olivier Mercier Peetz: Resource Gathering Server, Testing
