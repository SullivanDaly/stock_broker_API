# Stock Trading Platform

This Django-based project provides a simple stock trading platform where users can buy and sell stocks. The project also includes a feature to periodically update stock prices.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:
- Python (3.12 or higher)
- pip (Python package manager)
- Virtualenv (optional, but recommended)

or
- Docker
- Docker Compose

### Installing

Follow these steps to get your development environment running:

- **Clone the Repository**
git clone https://github.com/yourusername/stock-trading-platform.git
cd stock-trading-platform

### With Docker
1. **Build the Docker image**

This command builds the Docker image based on the Dockerfile and docker-compose.yml present in your project directory.
  ```
  docker-compose build
  ```

2. **Run the Docker container**

This command starts the container. The -d flag is used to run the container in detached mode, leaving the container running in the background.
  ```
  docker-compose up -d
  ```

3. **Create and apply migrations (Optional)**

After the container is running, you need to create and apply database migrations.
  ```
  docker-compose exec web python manage.py makemigrations
  docker-compose exec web python manage.py migrate
  ```

4. **Create a superuser (Optional, but recommended for accessing the admin panel)**

If you need to access the Django admin, create a superuser.
  ```
  docker-compose exec web python manage.py createsuperuser
  ```

5. **Flush Database (Optional)**
If you need to erase data from the database.
  ```
  docker-compose exec web python manage.py flush
  ```

6. **Populate Database (Optional)**
If you need to populate the databes with random data after erasing the database.
  ```
  docker-compose exec web python manage.py generate_data
  ```

### Without Docker

1. **Create and Activate Virtual Environment (Optional)** 

- For Unix or MacOS:
  ```
  virtualenv env
  source env/bin/activate
  ```

- For Windows:
  ```
  virtualenv env
  .\env\Scripts\activate
  ```

2. **Install Required Packages**
  ```
  pip install -r requirements.txt
  ```

3. **Run the Development Server**
  ```
  python manage.py runserver --noreload
  ```
The server will start at http://127.0.0.1:8000/


4. **Set Up the Database (Optional)** 

Run the following command to make migrations and migrate the database:
  ```
  python manage.py makemigrations
  python manage.py migrate
  ```

5. **Create Superuser (Optional, but recommended for accessing the admin panel)** 
  ```
  python manage.py createsuperuser
  ```
5. **Flush Database (Optional)**
If you need to erase data from the database.
  ```
  python manage.py flush
  ```

6. **Populate Database (Optional)**
If you need to populate the databes with random data after erasing the database.
  ```
  python manage.py generate_data
  ```

## Running the Tests

To run the automated tests for this system:

- **With Docker**
  ```
  docker-compose exec web python manage.py test
  ```

- **Without Docker**
  ```
  python manage.py test
  ```
