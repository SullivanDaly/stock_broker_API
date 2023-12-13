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
git clone https://github.com/SullivanDaly/stock_broker_API.git
cd stock_broker_API

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

## Views and Endpoints

This section explains the various views available in the application and how to interact with them. Our application provides RESTful endpoints for investors and admins to perform various operations.

### Authentication

- **Investor/Admin Login**
  - **Endpoint**: `broker_API/token/`
  - **Method**: POST
  - **Description**: Use this endpoint to authenticate as either an investor or an admin. It returns a JWT token for authenticated sessions.
  - **Data Format**: 
    ```json
    {
      "username": "your_username",
      "password": "your_password"
    }
    ```
  - **Response**: JWT Token
  - **Example Value**: Investor: "amoore:password", Admin: "ijones:password"

### Investor Operations

Investors can buy and sell stocks and view their portfolios. They must include the JWT token in the Authorization header for authentication.

- **Buy Stocks**
  - **Endpoint**: `/stocks/buy/`
  - **Method**: POST
  - **Authorization**: JWT Token required
  - **Description**: Allows investors to buy stocks. If the investor does not hold this type of stock already, a new portfolio is created; otherwise, the existing portfolio is modified.
  - **Data Format**: 
    ```json
    {
      "stock_name": "Wilson-Howard",
      "quantity": 10
    }
    ```
  - **Response**: Success or error message.

- **Sell Stocks**
  - **Endpoint**: `/stocks/sell/`
  - **Method**: POST
  - **Authorization**: JWT Token required
  - **Description**: Allows investors to sell stocks. If the investor sells all their stock, the portfolio is deleted; otherwise, it is modified.
  - **Data Format**: 
    ```json
    {
      "stock_name": "Wilson-Howard",
      "quantity": 5
    }
    ```
  - **Response**: Success or error message.

- **View Portfolio**
  - **Endpoint**: `/investor/portfolio/`
  - **Method**: GET
  - **Authorization**: JWT Token required
  - **Description**: Enables investors to view their current stock holdings.
  - **Response**: List of stocks in the portfolio.

### Admin Operations

Admins can create, edit, or delete stocks in the system. Admin actions also require JWT token for authentication.

- **Create New Stock**
  - **Endpoint**: `/stocks/create/`
  - **Method**: POST
  - **Authorization**: JWT Token required
  - **Description**: Allows admins to create new stock entries.
  - **Data Format**: 
    ```json
    {
      "name": "New Stock",
      "ticker_symbol": "NS",
      "description": "Description here",
      "price": 100.50
    }
    ```
  - **Response**: Details of the created stock or an error message.

- **Edit Stock**
  - **Endpoint**: `/stocks/edit/<name_or_symbol>/`
  - **Method**: PUT
  - **Authorization**: JWT Token required
  - **Description**: Allows admins to edit existing stock details.
  - **Data Format**: 
    ```json
    {
      "name": "Updated Stock Name",
      "description": "New description",
      "price": 110.00
    }
    ```
  - **Response**: Updated stock details or an error message.

- **Delete Stock**
  - **Endpoint**: `/stocks/delete/<name_or_symbol>/`
  - **Method**: DELETE
  - **Authorization**: JWT Token required
  - **Description**: Allows admins to remove a stock from the database.
  - **Response**: Success or error message.

### Error Handling
All endpoints return appropriate HTTP status codes and messages. In case of an error (like invalid credentials, insufficient permissions, or bad input data), the response will include a descriptive error message.