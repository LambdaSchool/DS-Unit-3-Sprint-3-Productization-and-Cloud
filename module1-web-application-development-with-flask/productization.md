# Productization == Deployment
    - putting MODELS into production so they can be used - software & hardware
    
# Front End / Back End

## Front
* Anything the user interacts with
* Markup and web languages: HTML, CSS, js

## Back
* Server architecture / database admin
* Programming & Scripting: Python, Ruby, Perl

# Deployment Methods

## 1. Cloud-Based

- these models live elsewhere

PMML - Predictive Model Markup Language (Older)
     * schema - structured set of rules 
     * txt file
     * model must be exported to PMML
     * requires a scoring engine
     
Serialization - Can be opened, used then closed
    * Scoring engine is not required
    * Flask acts as the middle layer between front & back

## 2. Local

## 3. Model Services

AWS - SageMaker
Microsoft - ML Studio Azure

# Flask

Web dev MicroFramework

In DS we use it to create APIs (expose endpoints to data)

Why?:
    * Simple to Learn
    * Extensively Scalable
    * Not Scaffolded - less dependency
    * Growing & Active Community
    
# Flask Concepts

* Apps - running as a service on a specific port

* Routes - pages or areas within the app

* Requests - GET/POST to/from the app

# Lecture

set up flask
small flask app
expand with routes
templates - render_templates

# API - Application Programming Interface

* access to a larger stack - twitter, facebook
* access to a data source
* middleware - for sending and receiving info