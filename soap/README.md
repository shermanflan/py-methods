# SOAP
Python proof of concept for interacting with SOAP web services.

## Features

- Using Zeep to interact with [SOAP services](utility/api/oracle.py)
    - Inspect WSDL
    - Import types
    - Invoke services
    - Download attachments
    - Examples use Oracle Fusion as a web service endpoint
- Utilities for uploading data to Azure [data lake](utility/api/lake.py)
- Utilities for publishing events to [Event Grid](utility/api/event.py)
- Example usage for Zeep via Jupyter [notebooks](jupyter/oracle_soap_ex.ipynb)

## Using [Zeep](https://docs.python-zeep.org/en/master/index.html)
Zeep facilitates interaction with SOAP services in a pythonic way.

- Inspect WSDL 
    - `python -mzeep https://myserver.com/fscmService/ErpIntegrationService?WSDL`