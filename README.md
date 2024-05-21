# License Plate Management System

## Description
This project is designed to manage customers and their respective license plates. It allows for adding, listing, and editing customers and license plates.

## Features
- Add customers and license plates
- Add and manage license plates for each customer
- List customers and license plates

## Technologies Used
- Django
- SQLite
- Docker

## Setup Instructions
### Pull repo
1. Clone the repository:
```sh
git clone https://github.com/goncalomi/b-parts.git
cd b-parts
```
### Using Docker (Recommended)
### Prerequisites
- Docker
- Docker Compose

### Steps
1. Build and run the Docker containers:
`docker-compose up --build`
### Without Docker
### Prerequisites
- Python 3.12+
- pip

2. Create and activate a virtual environment:
```sh
python -m venv venv
source venv/bin/activate   # On Windows use venv\Scripts\activate
```

3. Install dependencies
`pip install -r requirements.txt`

4. Run database migrations:
`python manage.py migrate`

5. Start the development server:
`sudo python manage.py runserver 80`

## Usage Instructions

### Adding a Customer and License Plates
1. Navigate to the homepage at http://localhost/
2. Click on "Add License Plate".
3. Enter the customer's email.
4. Add one or multiple license plates using the provided inputs.
5. Click "Save".

### Listing Customers and License Plates
1. Navigate to the homepage at http://localhost/
2. Click on "List License Plates".
3. View the list of customers and their license plates.
4. Each customer entry has an "Edit" button to manage license plates.

### Editing a Customer's License Plates
1. Click on the "Edit" button next to the customer in the list.
2. Add or remove license plates as needed.
4. Click "Save".

### Checking data in Django Admin
1. Navigate to the admin at http://localhost/admin
2. Login with the credentials:
    username: admin
    password: admin

## Testing

To run the tests with:
`python manage.py test cars/tests`
    
### Forms Tests
### CustomerFormTest
- Test with a valid customer email format.
- Test with an invalid customer email format.

### LicensePlateFormSetTest
- Test with a valid license plate inline formset.
- Test with an invalid license plate inline formset.
- Test creating a valid license plate.
- Test creating an invalid license plate.

### Models Tests
### CustomerModelTest
- Test creating a customer with a correct email format.
- Test creating a customer with a bad email format.

### LicensePlateModelTest
- Test creating a valid license plate with a user.
- Test creating a valid license plate without a user.
- Test creating a bad license plate with a user.
- Test creating an existing license plate with a user.

### Views Tests
### CustomerUpdateViewTest
- Test with a new customer and new license plate.
- Test with an invalid license plate.
- Test with an existing license plate.
- Test deleting a license plate.

### CustomerListViewTest
- Test listing customers and their license plates.


