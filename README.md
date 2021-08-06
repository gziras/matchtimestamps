### Installation

- Clone this repository and change to cloned directory
```
$ git clone https://github.com/gziras/matchtimestamps.git
$ cd matchtimestamps
```

### Python CLI
- Change to python3 directory and create virtual environment
```
$ cd python3
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

- Under the python3 directory, build image and run the docker container.
```
$ docker build -t local/periodic .
$ docker run --rm local/periodic --period 1d --t1 20201010T204603Z --t2 20201115T123456Z --tz Europe/Athens
```

### Go

- Run the program from the go directory. Provide IP and PORT as command line argument.
```
$ cd go
```
- Example Usage
```
$ go run script.go 0.0.0.0:8080 #<IP>:<PORT>
```
- Alternatively, build the executable and run it.
```
$ go build script.go
$ ./script :8080
```
 