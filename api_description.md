API Description

1) User Authentication Oauth2 with JWT







Micro Service 1: Ressource Gathering<br/>

| Methods             | HTTP   Request    |            Description             |
|---------------------|-------------------|------------------------------------|
| getRessourceInfo    | GET /ressources/  | Return ressource info by ressource |
| addRessourcerInfo   | POST /ressources/ | Insert ressource information       |
| ressourceUpdateInfo | PUT /ressource/   | Edit ressource profile or update   |

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




