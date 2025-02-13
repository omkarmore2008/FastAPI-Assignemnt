# FastAPI Assignment

This is a FastAPI application for managing items in a MongoDB database. It provides endpoints to create, read, update, and delete items and clock in.


## Requirements

- Python 3.7+
- FastAPI
- Pydantic
- Motor (MongoDB driver)
- Uvicorn (for running the server)
- PyMongo
- Bson

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/omkarmore2008/FastAPI-Assignemnt.git
    cd FastAPI-Assignemnt
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up MongoDB:
    - Ensure you have a running MongoDB instance.
    - Configure the connection string in the `app/config.py` file.

## Running the Application

To run the FastAPI application:

```bash
uvicorn app.main:app --reload
