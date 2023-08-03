# B3 Stock Wacher

## A user-friendly interface for configuring and monitoring assets from the B3 (Brazilian Stock Exchange), along with automatic price tracking and email notifications, assisting investors in making informed decisions based on the predefined price tunnel parameters.


# Features
The system is designed to obtain and store the price quotes of the registered assets from any public source, while adhering to the configured checking frequency for each asset. The web interface enables users to view and query the stored price data of the registered assets.

Additionally, the application automatically sends email notifications to the investor whenever the price of a monitored asset crosses its lower price tunnel limit, suggesting a buy opportunity. Similarly, it suggests a sell opportunity when the price of a monitored asset crosses its upper price tunnel limit.


# System design
The choice to use a Nuxt frontend in place of the Django templates was due to the support for modern javascript features and clear separation of concerns between frontend and backend. The priority of a web app will always be the user, being so, this approach permits the development of a mocked frontend design, enabling for faster feedback cycles for the actual product. Only after the frontend interface is validated will the backend development be initiated.


<p align="center">
  <img src="https://github.com/bennymirahy/b3_stock_watcher/blob/master/img/system_design.png?raw=true" />
</p>


# Backend design pattern
A MVC (Model-View-Controller) architecture was used. The Model represents the data and database schema. The View is responsible for the api interface, determining how information is presented to the users and how they interact with the application. The Controller part was implemented as a "services" file. It acts as an intermediary between the Model and View, handling the business logic. The Services file encapsulates the application's core functionalities, ensuring separation of concerns and making the codebase more organized and maintainable.

The choice for this structure was primarily for it's code reusability and scalability. The models, views, and services are loosely coupled, allowing for easier testing, debugging, and modifications without affecting other parts of the application.


# Development cycle
1. Implement your features on localhost:3001 (API Mock)
2. Validate that with a stakeholder (go back one step if needed)
3. Develop the back-end API for the feature
4. Check if everything is okay on the actual front-end on localhost:3000 (go back one step if needed)
5. Push your changes! \o/


# Dev commands
By running the shell script `dev.sh`, you'll have the following commands to help your development:

- **devhelp**: Print the help commands

- **dkdev**: Runs a dockerized *postgresql*, *nginx* and *metabase*

- **dkdb**: Runs a dockerized *postgresql* database on port 5432

- **dknginx**: Runs a dockerized *nginx* on port 80 to 8000 (back), 3000 (front), 3001 (mocked front)

- **pytest**: Runs python tests

- **pycoverage**: Runs python tests with flake8 and coverage report

- **dkbuild**: Builds a docker image for this project

- **dkfulldev**: Runs a dockerized *postgresql*, *nginx* and the project image