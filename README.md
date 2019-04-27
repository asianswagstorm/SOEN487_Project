# JAMDO
Private Repo for SOEN 487 Web Services Class Written in Flask

General project description:
Our web application leverages information retrieval returning engaging and compelling information based on the data and location of a users' data and place of birth. Given these two arguments the application will search and return a wide variety of relevant information to display to the user. A web crawler will be required to search and gather for information based on user inputs. This will entail utilizing existing 3rd party APIs as an efficient way of retrieving specific data. To optimize the web crawling, reduce requests, and lower wait times, previously searched information will be saved in persistent data. The managing of persistent data will require the creating of a caching engine to detect, return, and update data in the databases. Finally aside from a users' ability to query data and location, asynchronous requests will be made to give users an 'infinite scroll'. Here, extra requests for additional information will be made. Users may also be able to request specific information such as requesting more information on given lists, items, query other topics given the date and location.

The application utilizes four microservices to manage the resources and data it collects: resource gathering of relevant information, data caching of previously requested information, request processing, and continuous asynchronous requests.


Installation Instructions:



Instructions to run:

1)go into authentication folder
  run command 
  python main.py
  
2)go into resource gathering folder
  run command
  python main.py
  
3)go into caching folder
  run command 
  python main.py 
  
4)go into Jamdo folder
  run command
  python main.py


Contributors:
- James Edwards, jamesedwards1394@gmail.com
- Andy Nguyen, nguyen.andy123@gmail.com
- Manuel Toca, manueltoca03@gmail.com
- Nguyen Dinh, nguyen.andy123@gmail.com
- Olivier Mercier Peetz, oliviermercierpeetz@live.ca


Tasks breakdown, responsibilities:
- James Edwards: Caching server
- Andy Nguyen: Authentication server, Application Server
- Manuel Toca: Caching server
- Nguyen Dinh: Authentication server, Application Server
- Olivier Mercier Peetz: Resource Gathering Server


Known issues, bugs:



Other comments:





