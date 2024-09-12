# Project 
This project is a basic fullstack application that utilises fastapi for the backend, streamlit for the frontend and stores data in a data. My aim is was to upskill in building fullstack applications and learn more about financial tooling.

## Usage
To use this project you can go to the following [link](https://financial-engineering-flattened.streamlit.app/)
This version is flattened to use streamlit's services and doesn't utilise a database


### Local
1. Clone the repository using the following command:
  ```
  git clone <repository_url>
  ```

2. Navigate to the project directory:
  ```
  cd Financial_Engineering
  ```

3. Run the project using Docker Compose:
  ```
  docker-compose up
  ```

Alternatively, if you have a separate debug configuration file, you can use the following command:
  ```
  docker-compose -f docker-compose.debug.yml up
  ```

If you prefer to run the project using a launch configuration, you can configure your `launch.json` file accordingly.

Please note that you may need to install Docker and Docker Compose before running the project.
