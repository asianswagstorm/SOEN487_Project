API Description

1) User Authentication Oauth2 with JWT







Micro Service 1: Ressource Gathering



Methods	              HTTP            Request	                Description

getRessourceInfo	     GET             /ressources/	        Return ressource info by ressource id
getDataFromRessource   GET            /ressources/data      Returns json data from the ressource that matches "data"
addRessourceInfo	    POST            /ressources/	        Insert ressource information (API Url and parameters needed for query) 
ressourceUpdateInfo	   PUT             /ressource/	        Edit ressource profile or update ressource point

Example: Adding wikipedia as ressource and getting information

addRessourceInfo
  name of ressource : Wikipedia (ID:1)
  endpoint:  http://en.wikipedia.org/w/api.php 
  action=query  //to fetch data from wiki
  list=search   //to get list of pages matching a criteria
  srsearch=      //along with a page title to search for
  format=jsonfm   //recommended format for output


