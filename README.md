# Template Driver - FastAPI Implementation

This is a Python FastAPI port of the TemplateDriver shipping integration sample. It provides endpoints for setting up shipping integrations, generating labels, and creating manifests.

## Features

- User configuration and authentication
- Multi-stage configuration process
- Label generation for shipping packages
- Manifest creation and printing
- Support for extended properties

## Getting Started

### Prerequisites

- Python 3.9+
- pip

### Installation

1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure environment variables or create a `.env` file

### Running the Application

```bash
uvicorn app.main:app --reload
```

### API

The API will be available at http://localhost:8000

### API Documentation
Once running, you can access the Swagger UI docs at /docs or ReDoc at /redoc

### API Endpoints

#### Setup
* **POST**
 `/api/Setup/AddNewUser` - Create a new user account
* **POST**
 `/api/Setup/UserConfig` - Get user configuration
* **POST**
 `/api/Setup/UpdateConfig` - Update user configuration
* **POST**
 `/api/Setup/ConfigDelete` - Delete user configuration
* **POST**
 `/api/Setup/UserAvailableServices` - Get available services
* **POST**
 `/api/Setup/ExtendedPropertyMapping` - Get extended property mappings

#### Consignment
* **POST**
 `/api/Consignment/GenerateLabel` - Generate shipping labels
* **POST**
 `/api/Consignment/CancelLabel` - Cancel a shipping label

#### Manifest
* **POST**
 `/api/Manifest/CreateManifest` - Create a shipping manifest
* **POST** 
* `/api/Manifest/PrintManifest` - Print a shipping manifest