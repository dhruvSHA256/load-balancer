# Load Balancer
- my implementation of a layer 4 load balancer with health checks in python.
- currently Round Robin server selection algorithm is supported.

## Demo
- edit `config.json`
- run multiple servers on port defined in `config.json` in different terminal windows
```sh
# like this
python server.py 5001 # in one window
python server.py 5002 # in another window
```
- run load balancer
```sh
python loadbalancer.py PORT
```
- make a request to load balancer
```sh
curl localhost:PORT
```
- requests will be redirected to any of running backend server.
- if a server missed heartbeat of is offline, no new request will be sent to it.
- if a server came back online, new requests will be redirected to it.
- you can see asciicast [![here](https://asciinema.org/a/618289)](https://asciinema.org/a/618289)

[![asciicast](./demo.svg)](./demo.svg)


## Load Balancer vs Reverse Proxy
- Load Balancer is a Reverse Proxy with additional bells and whistles.

## Layer 4 vs Layer 7 load balancer

### Layer 4 Load Balancer
- Cant see the data of request, only binary.
- Data may be compressed, encrypted.
- It can only see src and dest ip.
- Change dest ip to server using NAT.
- Only one tcp connection.

### Layer 7 Load Balancer
- Can see the data of request and based on that redirects request.
- Like sending to server based on user id.
- Client request -> lb (can change request, add headers etc etc) -> lb make new request to server.

## Load Balancing Algorithms
- Round Robin.
- Weighted Round Robin.
- Lease Connection First.
- Lease Response Time First.
- Hash Based.
