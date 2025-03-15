# FastAPI CRUD Application

A simple CRUD application demonstrating FastAPI integration with PostgreSQL, featuring multiple user interfaces: command-line, Tkinter GUI, and PyQt.

## Overview

This application provides a complete example of creating a database-backed API with FastAPI that can be accessed through multiple interfaces. It demonstrates both query parameter and JSON-based REST API approaches.

## Features

- **FastAPI Backend** with automatic OpenAPI documentation
- **PostgreSQL Database** integration using psycopg2
- **Three User Interfaces**:
  - Command-line interface
  - Tkinter GUI
  - PySide6/PyQt GUI
- **CRUD Operations** (Create, Read, Update, Delete)
- **RESTful API Design**
- **Pydantic Models** for data validation

## Project Structure

```
src/
├── crud.py        # Database operations
├── dbconn.py      # Database connection management
├── interface.py   # Command-line interface
├── gui.py         # Tkinter GUI implementation
├── new_gui.py     # PySide6/PyQt GUI implementation
├── main.py        # FastAPI application
└── models.py      # Pydantic data models
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-crud-app.git
   cd fastapi-crud-app
   ```

2. Install dependencies:
   ```bash
   pip install requirements.txt
   ```

4. Set up PostgreSQL:
   - Create the table with:
     ```sql
     CREATE TABLE minha_tabela (
         id SERIAL PRIMARY KEY,
         nome VARCHAR(100) NOT NULL,
         idade INTEGER NOT NULL
     );
     ```
   - Update connection settings in crud.py if needed

## Usage

### Starting the API Server

```bash
fastapi dev main.py
```

#### Start one of the interfaces

ex:  
```bash
python new_gui.py
```

## API Endpoints
The API documentation will be available at http://127.0.0.1:8000/docs  

### REST-Style Endpoints (JSON)

- **GET /items** - List all records
- **GET /items/{item_id}** - Get specific record
- **POST /items** - Create new record (JSON body)
- **PUT /items/{item_id}** - Update record (JSON body)
- **DELETE /items/{item_id}** - Delete record

### Query Parameter Endpoints

- **GET /select** - List all records
- **POST /insert?nome=value&idade=value** - Create record
- **PUT /update?id=value&nome=value&idade=value** - Update record
- **DELETE /delete?id=value** - Delete record


## License

MIT License

## Contributing

Contributions, issues, and feature requests are welcome!
