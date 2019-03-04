## Overview

Our web application leverages information retrieval returning engaging and compelling information based on the data and location of a users\' data and place of birth. Given these two arguments the application will search and return a wide variety of relevant information to display to the user. A web crawler will be required to search and gather for information based on user inputs. This will entail utilizing existing 3rd party APIs as an efficient way of retrieving specific data. To optimize the web crawling, reduce requests, and lower wait times, previously searched information will be saved in persistent data. The managing of persistent data will require the creating of a caching engine to detect, return, and update data in the databases. Finally aside from a users'' ability to query data and location, asynchronous requests will be made to give users an \'infinite scroll\'. Here, extra requests for additional information will be made. Users may also be able to request specific information such as requesting more information on given lists, items, query other topics given the date and location. The application will utilize four microservices to manage the resources and data it collects; resource gathering of relevant information, data caching of previously requested information, request processing, and continuous asynchronous requests.


## Application Public Endpoints
The following table represents the public API endpoints. Listed are both the URI which browsers will use and the application will hyperlink returning a HTML document. Alternatively, an the `/api/` in the URI will signal the server to respond with the raw JSON information as a response. Location data will be added to these endpoints via URL queries and will be further processed by the server.
ex. `http://www.JAMDO.com/api/2002/10/28?location=Berlin,Germany`

| HTTP METHOD | URL                       | Description                                      |
|-------------|---------------------------|--------------------------------------------------|
| GET         | /<Year>                   | Returns HTML based on given year                 |
| GET         | /<Year>/<Month>           | Returns HTML based on given year and month       |
| GET         | /<Year>/<Month>/<Day>     | Returns HTML based on given year, month, and day |
| GET         | /api/<Year>               | Returns JSON based on given year                 |
| GET         | /api/<Year>/<Month>       | Returns JSON based on given year and month       |
| GET         | /api/<Year>/<Month>/<Day> | Returns JSON based on given year, month, and day |


## Micro Service 1: Resource Gathering

| Methods              | HTTP   Request       |            Description                  |
|----------------------|----------------------|-----------------------------------------|
| getResourceInfo     | GET /resources/     | Return resource info by resource id   |
| getDataFromResource | GET /resources/data | return matching data from resource API |
| addResourcerInfo    | POST /resources/    | Insert resource information            |
| resourceUpdateInfo  | PUT /resource/      | Edit resource profile                  |

Example: Adding wikipedia as ressource and getting information<br />


Method : addRessourceInfo<br />
  name of ressource : Wikipedia (ID:1)<br />
  endpoint:  http://en.wikipedia.org/w/api.php <br />
  action=query  //to fetch data from wiki<br />
  list=search   //to get list of pages matching a criteria<br />
  srsearch=      //along with a page title to search for<br />
  format=jsonfm   //recommended format for output<br />
  
Method : getDataFromRessource       /ressource/data      data=John
Queries wikipedia API for John
http://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=John&format=jsonfm


## Micro Service 2: Authentication Oauth2 and JWT<br/>

| Methods              | HTTP   Request       |            Description                  |
|----------------------|----------------------|-----------------------------------------|
| login                | POST auth/login          | Verify login credentials match info in db  |
| register             | POST auth/register       | Adds the user to database along with a token |
| logout               | - /logout            | Deletes the session and clear the token |
| refreshToken         | GET auth/login           | Get a new access token without having to reauthenticate|

## References
https://gsa.github.io/api-documentation-template/api-docs/
