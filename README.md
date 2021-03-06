<h1><img src="./img/logo.png"></h1>
 <img src="https://img.shields.io/badge/Contributors-4-yellow.svg">

## What is this?

> Drug Precautions Retrieval Service

### Function

* Medication search (automated search term)
* Prescription Image Drag & Drop Function
* Extraction of Medication codes through OCR API
* Retrieve cautions for medicines



## Stack

> Front-end

* Vue.js
* HTML5 / CSS3 / JavaScript / jQuery / Ajax

> Back-end

* Django 2.2.7
* python 3.7.4
* SQLite



## Installation

1. https://github.com/kyun9/Medignore.git  - [Clone or download] - ["Click"]

   

## Usage

1. Create a python virtual environment

   ```bash
   $ python -m venv venv
   $ source ./venv/Scripts/activate
   ```

2. Adding python package

   ```bash
   $ pip install -r requirements.txt
   ```

3. Apply Migration

   ```bash
   $ python manage.py migrate
   ```

4. Create .env file

   ```
   DATA_API_SERVICEKEY="{DATA_API_SERVICEKEY}"
   
   #KAKAO_VISION_API_KEY
   KAKAO_KEY="{KAKAO_KEY}"  
   ```

5. Running a server

   ```bash
   $ python manage.py runserver
   ```



## Screenshots

<img src="./img/medignore1.PNG">

<img src="./img/medignore4.PNG">



## Link

URL : [medignore](http://medignore.herokuapp.com/medignore/)