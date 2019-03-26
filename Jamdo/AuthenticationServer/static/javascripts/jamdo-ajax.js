/*
---Jamdo: Async Request Microservice---

Description:
This script runs in the background detecting the scroll position of the window. 
When the client is at the bottom of the content, the script makes a request to the application server 
for a randomized day/event to show to the user. Ideally, something already in the database to so the 
return is quick.

 */

// Check scroll position
// https://stackoverflow.com/questions/9439725/javascript-how-to-detect-if-browser-window-is-scrolled-to-bottom
window.addEventListener("scroll", function(){
  if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
    console.log('End of Page: Making request to Application Server');
    getNewDate();    
  }  
}, false);

// Make server request for more content
// https://developer.mozilla.org/en-US/docs/Web/Guide/AJAX/Getting_Started
function getNewDate(){
  let httpRequest;
  let container = document.getElementById('inf_scroll_container');
  let content = document.getElementById('inf_scroll_content');
  let loader = document.getElementById('lds-dual-ring');

  function toggleLoader(){
    loader.classList.toggle('show_loader');    
  }

  function makeRequest() {
    toggleLoader();
    httpRequest = new XMLHttpRequest();

    if (!httpRequest) {
      alert('Error: Cannot create an XMLHTTP instance');
      return false;
    }
    httpRequest.onreadystatechange = alertContents;
    httpRequest.open('GET', 'https://jsonplaceholder.typicode.com/comments?postId=1');
    httpRequest.send();
  }

  function alertContents() {
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
        toggleLoader();
        content.innerHTML = httpRequest.responseText;
      } else {
        toggleLoader();
        content.innerHTML += 'Error: There was a problem with the request.';
      }
    }
  }
  makeRequest();
}
