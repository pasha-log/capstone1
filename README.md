# The Carbon Print Calculator



https://user-images.githubusercontent.com/65935072/201440457-98b95105-6c1d-4248-9efb-c97ab90ba928.mp4


## Heroku site:
- 🌐[Carbon Print](https://carbonprint.herokuapp.com/)

## API Integration: 
This will be my first capstone project using a RESTful API called Carbon Interface: 
- 👣[Carbon Interface](https://docs.carboninterface.com/)

This simple application will utilize this API and provide a friendly UI to calculate a client's carbon footprints from activities such as 
* Vehicles
* Shipping  
* Flights
* Electricity 

## Technology Stack: 
* Frontend: HTML5, CSS3, jQuery, ES6, Vanilla JavaScript
* Backend: Python, Flask, SQLAlchemy, Postgres
* Libraries & modules: Chart.js, WTForms, Bcrypt, requests, unittest
* Templating engine: Jinja2

## How To Use:
Users are able to create an account and have four forms to choose from: vehicles, shipping, flights, and electricity. The vehicles form will first have you choose a brand and model of a vehicle (hundreds to choose from). I implemented this feature through making a JavaScript Async&Await fetch request to the Carbon Interface API and used DOM manipulation to dynamically append models to a select dropdown menu after the selection of a brand is made. From this user interaction, a vehicle model id is then obtained and the page gets redirected to the rest of the form. User is asked for the distance traveled on their vehicle, and choose which distance units and carbon dioxide measurements they want as their emission. After submit, users are taken to a result page showing their emission amount released into the atmosphere. The other three emission types follow a similar user flow. 

This application stores your emissions in a SQL database, and with Chart.js users can see the emissions they've created over time driving in their vehicles, creating a visual element to the emissions we make on a daily basis. The vehicle, shipping, and electricity carbon footprint estimates are calculated through Carbon Interface with Python requests. 


