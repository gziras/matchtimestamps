### Installation
TODO
- Clone this repository and change to cloned directory
```
$ git clone git://github.com/htr-tech/zphisher.git
$ cd zphisher
```

### Python CLI
- Create virtual environment
```
$ python3 -m venv env
```
- Install necessary packages
```
$ pip install python-dateutil pytz
```
- Example Usage
```
$ python3 script.py --help
$ python3 script.py --period 1d --t1 20201010T204603Z --t2 20201115T123456Z --tz Europe/Athens 
```


### Run on Docker (Python)

- Build image locally and run the docker container
```
$ docker build -t local/periodic .
$ docker run --rm local/periodic --period 1d --t1 20201010T204603Z --t2 20201115T123456Z --tz Europe/Athens
```
- Alternatively, run the docker container directly from Docker Hub.
TODO
```
$ docker run --rm local/periodic --period 1d --t1 20201010T204603Z --t2 20201115T123456Z --tz Europe/Athens
```

### Go

### 