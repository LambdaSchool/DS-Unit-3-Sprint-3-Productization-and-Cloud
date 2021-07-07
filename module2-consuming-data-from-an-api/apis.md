# Application Programming Interface

Not a DB or even a Server

It's the code that GOVERNS THE ACCESS POINTS for the server.

## Access an API

* Secure access - Twitter API
    Access and Auth Keys    
* Open Access - weather
    No Keys required
    
## JSON - JavaScript Object Notation

Most widely used format for data exchange

Common currency between processes or devices

Browser is the bottleneck

### Structures

1. Name, Value pairs - like a dictionary
2. Ordered list of values (array or list)

Linters - Reformat messy JSON files

## Requests

pip install requests

* GET
* POST
* PUT
* DELETE
* HEAD
* PATCH
* OPTIONS

Info for Request is sent in the URL

## Responses

* 200 - everything's good, connection made
* 301 - redirected to a different endpoint
* 400 - bad request
* 401 - authentication error - no access
* 403 - access is forbidden
* 404 - resource not found
* 451 - unavailable for legal reasons

All responses have a **HEADER**

## Dumps and Loads

