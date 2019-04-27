# JAMDO
Private Repo for SOEN 487 Web Services Class Written in Flask

General project description:
- Our web application leverages information retrieval returning engaging and compelling information based on the data and location of a users' data and place of birth. Given these two arguments the application will search and return a wide variety of relevant information to display to the user. A web crawler will be required to search and gather for information based on user inputs. This will entail utilizing existing 3rd party APIs as an efficient way of retrieving specific data. To optimize the web crawling, reduce requests, and lower wait times, previously searched information will be saved in persistent data. The managing of persistent data will require the creating of a caching engine to detect, return, and update data in the databases. Finally aside from a users' ability to query data and location, asynchronous requests will be made to give users an 'infinite scroll'. Here, extra requests for additional information will be made. Users may also be able to request specific information such as requesting more information on given lists, items, query other topics given the date and location.

- The application utilizes four microservices to manage the resources and data it collects: resource gathering of relevant information, data caching of previously requested information, request processing, and continuous asynchronous requests.


Installation Instructions:
1. Go into authentication folder and run main.py
2. Go into resource gathering folder and run main.py
3. Go into caching folder and run main.py
4. Go into Jamdo folder and run main.py

Contributors:
- James Edwards, jamesedwards1394@gmail.com
- Andy Nguyen, nguyen.andy123@gmail.com
- Manuel Toca, manueltoca03@gmail.com
- Nguyen Dinh, nguyen.andy123@gmail.com
- Olivier Mercier Peetz, oliviermercierpeetz@live.ca


Tasks breakdown, responsibilities:
- James Edwards: Caching server, Testing, Presentation
- Andy Nguyen: User Login/Registration, Application Server, Testing, Presentation
- Manuel Toca: Caching server, Testing, Presentation
- Nguyen Dinh: Authentication server, Application Server, Testing, Presentation
- Olivier Mercier Peetz: Resource Gathering Server, Testing


Known issues, bugs:
- Cache system does not consider updated Wiki information
- Some dates do not return any information
- There is no information for Years before 1900 and after 2018
- There is no information for births after 2001
- Returned information formatting can be messy




Other comments:





