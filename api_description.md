### Overview

Our web application leverages information retrieval returning engaging and compelling information based on the data and location of a users\' data and place of birth. Given these two arguments the application will search and return a wide variety of relevant information to display to the user. A web crawler will be required to search and gather for information based on user inputs. This will entail utilizing existing 3rd party APIs as an efficient way of retrieving specific data. To optimize the web crawling, reduce requests, and lower wait times, previously searched information will be saved in persistent data. The managing of persistent data will require the creating of a caching engine to detect, return, and update data in the databases. Finally aside from a users'' ability to query data and location, asynchronous requests will be made to give users an \'infinite scroll\'. Here, extra requests for additional information will be made. Users may also be able to request specific information such as requesting more information on given lists, items, query other topics given the date and location. The application will utilize four microservices to manage the resources and data it collects; resource gathering of relevant information, data caching of previously requested information, request processing, and continuous asynchronous requests.


### Application Public Endpoints

The following table represents the public API endpoints. Listed are both the URI which browsers will use and the application will hyperlink returning a HTML document. Alternatively, an the `/api/` in the URI will signal the server to respond with the raw JSON information as a response. Location data will be added to these endpoints via URL queries and will be further processed by the server.

ex. `http://www.JAMDO.com/api/2002/10/28?location=Berlin,Germany`

| HTTP METHOD | URL                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET         | /:Year                  | Returns HTML based on given year                 |
| GET         | /:Year/:Month           | Returns HTML based on given year and month       |
| GET         | /:Year/:Month/:Day     | Returns HTML based on given year, month, and day |
| GET         | /api/:Year               | Returns JSON based on given year                 |
| GET         | /api/:Year/:Month       | Returns JSON based on given year and month       |
| GET         | /api/:Year/:Month/:Day | Returns JSON based on given year, month, and day |


### Micro Service 1: Resource Gathering

| Methods              | HTTP   Request       |            Description                  |
|----------------------|----------------------|-----------------------------------------|
| return_event_day     | GET /event_type/year/month/day  | Return all information on that day from wiki in json format  |
| return_event_month   | GET /event_type/year/month/ | Return all information on that month from wiki in json format |
| return_event_year    | GET /event_type/year/    | Return all information on that year from wiki in json format     |


Example: Getting the event_type information for a specific day<br />


Method : return_event_day<br />
  route : /event_type/year/month/day<br />
  event_type:  can be event, birth or death <br />
  event : historical event(s) that happened that date <br />
  birth : birth(s) that happened that date <br />
  death : deaths(s) that happened that date <br />
  input example : /birth/1948/1/2 
  


### Micro Service 2: Authentication Oauth2 and JWT<br/>

| Methods              | HTTP   Request       |            Description                  |
|----------------------|----------------------|-----------------------------------------|
| login                | POST /login          | Verify login credentials match info in db  |
| register             | POST /register       | Adds the user to database along with a token |
| logout               | - /logout            | Deletes the session and clear the token |
| users                | GET /users           | A protected page only restricted for Admin to manage users|



## Technical Microservice Description:
#### 1. Resource Gathering Server
- This microservice responds to HTTP requests describing a date. Given these parameters predetermined 3rd party APIs will be queried to generate a list of interesting information. Authenticated requests will signal to the service that the request was made by the caching system. 

| Request | Response                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /:Year/:Month/:Day         | 200 JSON                  | Formatted JSON response of 3rd party API data                 |
| GET /:Year/:Month/:Day  (**Authenticated**)        | POST -> Cache Server           | Store processed 3rd party API data       |

#### 2. Data Persistance/Caching Server
- The Caching Server describes the state of the persistant data retrieved from the Resource Server. Dates not present in the database are expected to be populated by the Resource Server.

| Request | Response                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /:Year/:Month/:Day         | 200 JSON                  | Query of data in database                 |
| POST (**Authenticated**)        | 200 JSON, POST -> Application Server          |Response of successful data store, Signals newly saved| 

#### 3. Authentication Server
- This server verifies that certain requests are made by Application microservices. Authenticated requests will produce specific functions from the server.

| Request | Reponse                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /getToken/:ServiceID        | 200 JSON                  | Gives microservice server unique token                 |
| GET /authenticate/:ServiceID        | 200 JSON          |Validates service ID from token|

#### 4. Asynchronous Requests
- This front-end microservice detects user interactions and creates background requests to continuously generate content for Client

| Request | Reponse                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /:Year/:Month/:Day?Location=Location&Pagination         | --                  | Makes background HTTP requests to Application Server                 |

#### 5. Application Server
- The hub that connects the user interface to the the 3rd Party API data.

| Request | Reponse                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET /:Year/:Month/:Day?Location=Location&Pagination         | GET /:Year/Month/Day?Location=Location -> Cache Server 
GET /:Year/Month/Day?Location=Location -> Resource Server
| Checks Caching Server for date in data, Makes request to Resource Server for data
| GET /cache/:Year/:Month/:Day            | -- | Validates date storage, adds to potential local mem list
| POST /:Year/:Month/:Day            | 200 HTML | JSON 3rd API data (from Resource or Cache Server) applied to template view for client|


## Milestones
- Trace for getting Top 10 Books for date returned to user
  1. *Front-end* request of date
  2. *Application server* query of *Caching Server*
  3. Authentication of request from *Application Server*
  4. Reponse of cached date (cache miss)
  4. *Application Server* request for resources from *Resource Server*
  5. Authentication of *Application Server*
  6. Gathering/Processing of data from 3rd party APIs
  7. *Resource Server* POST request of processed data to *Cache Server*
  8. *Resource Server* JSON response to *Application Server*
  9. Processing of response JSON to Applicatio View Template
  10. HTML Response to Client

### References
https://gsa.github.io/api-documentation-template/api-docs/
