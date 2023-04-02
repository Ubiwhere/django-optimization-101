# Django Optimization 101 :rocket:
Welcome to the Django Performance Optimization Workshop! :tada:

This repository contains the code used in the workshop presentation, which covers different techniques to optimize the performance of Django REST APIs. These techniques include queryset optimization, database indexing and caching.

## Setup :computer:
To run this code on your local machine, follow these simple steps:

1. Make sure you have Docker and Docker Compose installed on your machine.
2. Clone this repository to your local machine.

```sh
git clone https://github.com/Ubiwhere/django-optimization-101
```

3. Open your terminal, navigate to the repository folder, and run the following command:
```sh
docker-compose up --build -d
```

This command will set up all the necessary services (Django API, database, Redis for cache), install Django Debug Toolbar, and generate mock data.

## Presentation :speech_balloon:
If you want to follow along with the presentation, you can access it on Canva using this [link](https://www.canva.com/design/DAFewtXti2g/YwDSO00jHC3zPWPKHKNjJw/view?utm_content=DAFewtXti2g&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton) :point_left:

## API Documentation :book:
The API endpoints are documented using Swagger and can be accessed at [http://localhost:8000/api](http://localhost:8000/api/) once you start the application.

Let's get optimizing! :fire: :fire: :fire:

## License
This code is released under the MIT License. See LICENSE for more information.