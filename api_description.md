API Description

1) User Authentication Oauth2 with JWT







Micro Service 1: Ressource Gathering

<pre>

Methods         HTTP          Request        Description<br />

getRessourceInfo          GET         /ressources/          Return ressource info by ressource id<br />
getDataFromRessource          GET         /ressources/data          Returns json data from the ressource that matches "data"<br />
addRessourceInfo          POST          /ressources/          Insert ressource information (API Url and parameters needed for query) <br />
ressourceUpdateInfo         PUT         /ressource/         Edit ressource profile or update ressource point<br />

Example: Adding wikipedia as ressource and getting information<br />


Method : addRessourceInfo<br />
  name of ressource : Wikipedia (ID:1)<br />
  endpoint:  http://en.wikipedia.org/w/api.php <br />
  action=query  //to fetch data from wiki<br />
  list=search   //to get list of pages matching a criteria<br />
  srsearch=      //along with a page title to search for<br />
  format=jsonfm   //recommended format for output<br />


