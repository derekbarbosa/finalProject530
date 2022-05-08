<!--
Hey, thanks for using the awesome-readme-template template.  
If you have any enhancements, then fork this project and create a pull request 
or just open an issue with the label "enhancement".

Don't forget to give this project a star for additional support ;)
Maybe you can mention me or this repo in the acknowledgements too
-->
<div align="center">

  <h1>🚙 Travel There Yourself 🚗</h1>
  
  <p>
    An all-in-one self-service travel application
  </p>
  
</div>


<!-- Table of Contents -->
# :notebook_with_decorative_cover: Table of Contents

- [:notebook_with_decorative_cover: Table of Contents](#notebook_with_decorative_cover-table-of-contents)
  - [:star2: About the Project](#star2-about-the-project)
    - [📱: API Documentation](#iphone-api-documentation)
    - [:dart: Features](#dart-features)
  - [:toolbox: Getting Started](#toolbox-getting-started)
    - [:bangbang: Prerequisites](#bangbang-prerequisites)
    - [:running: Run Locally](#running-run-locally)
  - [:compass: Roadmap](#compass-roadmap)
  - [:gem: Acknowledgements](#gem-acknowledgements)

  

<!-- About the Project -->
## :star2: About the Project

The goal of this project is to implement an all inclusive, self-service mobile application for travel planning. Many applications and websites such as kayak, expeida, and Google do bookings for accomodations, rentals, and flights, but do not have an easy to use platform for budgeting alongside planning. This application solves that problem. Travel There Yourself (TTY) gives users an easy to use platform for planning their vacations, road trips, and weekend getaways, keeping costs transparent so users can spend as little or as much as possible. 

<!-- APIs Documentation -->
### 📱: API Documentation

All APIs developed for this application are deployed via Flask REST Framework for Python on AWS EC2. We use the Google Maps API to give directions and hotel information to users. Apis are listed below:
- AddUser
  - Post: add a user to the application's MongoDB Users collection.
    - Arguments: Username, Password, Email, 
    - Return values: "User successfully added" or "User already exists"
  - Get: check if a user already exists in the database
    - Arguments: Username, Password, Email
    - Return values: 1 on success, 0 if User doesn't exists
   
- AuthenticateUser
  - Get: Authenticate a User on login to the application
    - Arguments: Username, Password
    - Return values: 1 on success, 0 on failure


- AddTrip
  - Post: add a trip to the application's MongoDB Trips collection
    - Arguments: username, destination, departure date, return date, airline (yet to implement flights funtionality), hotel
    - Return values: "Trip to {destination} added" or "Trip to {destination} already exists"
 
- GetTrip
  - Get: Retrieve a User's trip from the database
    - Arguments: username, destination, departure date
    - Return values: JSON containing matching trip data for arguments

- FindHotels
  - Get: Uses google maps API to retrieve a specified number of closest hotels to a specified destination
    - Arguments: destination, num_hotels
    - Return values: JSON structure containing the specified number of closest hotels and their address, rating, and an image

- GetDirections
  - Get: Uses google maps API to get the driving directions from a specified origin to a destination
    - Arguments: origin, destination
    - Return values: trip distance, trip destination, html verbose directions

- GetGasCost
  - Get: Uses EIA API to estimate the total gas cost of a trip based on the day's median gas price
    - Arguments: origin, destination, gas tank size, miles per gallon (mpg)
    - Return value: dollar value of estimated cost (int)
  
<!-- Features -->
### :dart: Features

- User Authentication using MongoDB
- Trip route planning using Google Maps API
- Hotel search feature using Google Geocode and Maps APIs
- Gas cost calculator using EIA API


<!-- Getting Started -->
## 	:toolbox: Getting Started

<!-- Prerequisites -->
### :bangbang: Prerequisites

This project uses PIP as package manager, it is recommended that you use a [VirtualEnv](https://docs.python.org/3/library/venv.html) for this app!

Please esnure you have Python version 3.9.10 or greater (and the latest version of pip)!

Tested on MacOS Big Sur and Windows 10

   
<!-- Run Locally -->
### :running: Run Locally

Clone the project

```bash
  git clone https://github.com/derekbarbosa/finalProject530
```

Go to the backend directory

```bash
  cd backend
```

Install dependencies via the requirements.txt file provided
```bash
 pip install -r requirements.txt
```

Run Tests in Tests Folder

```bash
  python test_user.py
  python test_trips.py
```

<!-- Roadmap -->
## :compass: Roadmap

* [x] User Authentication Module
* [x] Trip Storage Module
* [x] Google Maps API Integration
* [x] Flask Deployment
* [ ] Vue.js Frontend
* [ ] Google Flights Functionality
* [ ] Show Gas Stations on a Route
* [ ] EV Compatibility


<!-- Acknowledgments -->
## :gem: Acknowledgements

Some incredible resources everyone should check out ;) 
 - [Awesome README](https://github.com/matiassingers/awesome-readme)
 - [Emoji Cheat Sheet](https://github.com/ikatyang/emoji-cheat-sheet/blob/master/README.md#travel--places)
 - [Readme Template](https://github.com/othneildrew/Best-README-Template)


