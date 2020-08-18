# Simple Insurance
MVP case with a service for calculating the cost of insurance 
depending on the type of cargo and the declared value

### Installation

Simple-insurance requires [Docker](https://www.docker.com/get-started) to run.

Upload the repository to a local machine.

```sh
$ git clone https://github.com/dormantman/simple-insurance
```

Install the dependencies and start the server.

```sh
$ docker-compose build
$ docker-compose up -d
```

You can change the settings. the configuration file is located in [/app/config.py][config]

License
----

MIT


**Free Software, Hell Yeah!**


[config]: <https://github.com/dormantman/simple-insurance/blob/master/app/config.py>