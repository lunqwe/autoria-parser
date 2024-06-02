```markdown
# Auto.RIA Ad Scraper

This is an application for parsing ads on the site [https://auto.ria.com](https://auto.ria.com).

The application uses Selenium to retrieve data from the site and SQLAlchemy to work with the database (SQLite for local development, PostgreSQL to run the application in Docker-compose).

## Project Structure

### database
Module for working with and processing the database.
- **config.py** - for setting up the database
- **models.py** - for describing models (In this case, I created a Card model, the fields of which correspond to the technical specifications)

### scrapper
Functional module for obtaining information from the site.
- **main.py** - to launch the parser itself
- **scrapper.py** - a file that implements the Scrapper class, which contains functions for receiving and processing data from the site (auto.ria)

## Launch

To run the application you will need to:
1. Clone the repository
2. Run Docker Compose with the command:
    ```sh
    docker-compose up --build
    ```
    (P.S. To run the project you will also need to install Docker on your PC)

### Running Locally

You can also run the project locally (without using Docker). For this:
1. Install dependencies:
    ```sh
    pip install -r req.txt
    ```
2. Run the `run.py` file:
    ```sh
    python run.py
    ```

That's all!
```
