# Project: Database Sharding

The purpose of this project is to build a scalable and efficient database solution using horizontal sharding and Docker. The project will utilize Docker Compose to create and manage the MaxScale container as the database proxy and MariaDB containers that make up the sharded database.

The [Python script](./maxscale/main.py) will demonstrate how multiple database shards can be queried as if the sharded database was a single database, allowing for improved performance and reliability as the volume of data grows.

## Configuration

**BEFORE PROCEEDING**: The following will be done on Ubuntu 18.04.

Installing Docker:
A guide can be found [here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04). If you're on a different OS or version, please look for another guide before proceeding.

Installing Docker Compose:
```
sudo apt install docker-compose
```

Installing MySQL Connector package:
```
sudo apt install python3-pip
pip3 install mysql-connector
```

**BEFORE PROCEEDING**: The MaxScale container must have been created before running the following command. Skip to the [MaxScale Docker-Compose Setup](https://github.com/6ri4n/maxscale-docker#maxscale-docker-compose-setup) section and return to step 1 once you have the Docker-Compose up.

Editing the Python script to contain the correct ip address of the MaxScale container:
1. Identifying the ip address of the MaxScale container:
```
docker inspect maxscale_maxscale_1
```

A JSON object will be returned, here's part of it:
```
"maxscale_default": {
                    "IPAMConfig": null,
                    "Links": null,
                    "Aliases": [
                        "223e917119b5",
                        "maxscale"
                    ],
                    "NetworkID": "63196d15cb1a34715db7897067b7432b52e172961fc7929df850159ebe52144d",
                    "EndpointID": "019f17c980d55f6a7f4ec07750b12e46804a99a5d0dbf1f323d06f1a78bd17be",
                    "Gateway": "172.18.0.1",
                    "IPAddress": "172.18.0.4",
                    "IPPrefixLen": 16,
                    "IPv6Gateway": "",
                    "GlobalIPv6Address": "",
                    "GlobalIPv6PrefixLen": 0,
                    "MacAddress": "02:42:ac:12:00:05",
                    "DriverOpts": null
                }
```

2. Look for the following JSON property **"IPAddress": "172.18.0.4"** near the bottom and take note of the ip address. This is the IP address that you will edit into the Python script.

3. Navigate to the [maxscale](./maxscale/) directory.

4. Use a text editor (I'll be using nano) to edit the main.py file located in the current directory.
```
nano main.py
```

5. Go to line 22 (**host = '172.18.0.4',**) and check if the ip address matches with the ip address from step 2, if not please edit the ip address. The ip address should be within the single quotes. Save your changes and exit from the text editor (CTRL + O and CTRL + X).

You can now [run](https://github.com/6ri4n/maxscale-docker#running) the Python script.

## MaxScale Docker-Compose Setup

The [MaxScale docker-compose](./maxscale/docker-compose.yml) setup contains MaxScale
configured with a three node primary-replica cluster. 

## MaxScale Docker-Compose Setup

The [MaxScale docker-compose](./maxscale/docker-compose.yml) setup contains MaxScale
configured with a three node primary-primary cluster.

**BEFORE PROCEEDING**: The following commands assume the user is in the docker group, if not, use "**sudo**" before each command.

The following commands should be executed within the [maxscale directory](./maxscale/):

Starting MaxScale with its primary-primary cluster:
```
docker-compose up -d
```

Viewing the status of the cluster:
```
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬──────────┬──────┬─────────────┬─────────────────┬──────────┬─────────────────┐
│ Server  │ Address  │ Port │ Connections │ State           │ GTID     │ Monitor         │
├─────────┼──────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server1 │ primary1 │ 3306 │ 0           │ Master, Running │ 0-3000-5 │ MariaDB-Monitor │
├─────────┼──────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server2 │ primary2 │ 3306 │ 0           │ Running         │ 0-3001-5 │ MariaDB-Monitor │
└─────────┴──────────┴──────┴─────────────┴─────────────────┴──────────┴─────────────────┘
```

Removing MaxScale and its cluster containers:
```
docker-compose down -v
```

## Running

**BEFORE PROCEEDING**: Everything in the [Configuration](https://github.com/6ri4n/maxscale-docker#configuration) section must have been completed.

The purpose of the Python script is to interact with and query the sharded database created using Docker Compose.

The following command should be executed within the [maxscale directory](./maxscale/):

Running the Python script:
```
python3 main.py
```

Output from the script:
```
1. Retrieve the last 10 rows of data from the zipcodes_one shard.

(47731, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47732, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47733, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47734, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47735, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47736, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47737, 'PO BOX', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47740, 'UNIQUE', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47747, 'UNIQUE', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')
(47750, 'UNIQUE', 'EVANSVILLE', 'IN', 'PRIMARY', '37.98', '-87.54', 'NA-US-IN-EVANSVILLE', 'FALSE', '', '', '')

2. Retrieve the first 10 rows of data from the zipcodes_two shard.

(38257, 'STANDARD', 'SOUTH FULTON', 'TN', 'PRIMARY', '36.49', '-88.88', 'NA-US-TN-SOUTH FULTON', 'FALSE', '2066', '3778', '63816233')
(40022, 'STANDARD', 'FINCHVILLE', 'KY', 'PRIMARY', '38.15', '-85.31', 'NA-US-KY-FINCHVILLE', 'FALSE', '437', '839', '19909942')
(40023, 'STANDARD', 'FISHERVILLE', 'KY', 'PRIMARY', '38.16', '-85.42', 'NA-US-KY-FISHERVILLE', 'FALSE', '1884', '3733', '113020684')
(40025, 'PO BOX', 'GLENVIEW', 'KY', 'PRIMARY', '38.3', '-85.65', 'NA-US-KY-GLENVIEW', 'FALSE', '', '', '')
(40026, 'STANDARD', 'GOSHEN', 'KY', 'PRIMARY', '38.4', '-85.59', 'NA-US-KY-GOSHEN', 'FALSE', '2340', '4686', '154893571')
(40027, 'PO BOX', 'HARRODS CREEK', 'KY', 'PRIMARY', '38.28', '-85.62', 'NA-US-KY-HARRODS CREEK', 'FALSE', '', '', '')
(40031, 'STANDARD', 'LA GRANGE', 'KY', 'PRIMARY', '38.4', '-85.37', 'NA-US-KY-LA GRANGE', 'FALSE', '8322', '15818', '383923762')
(40032, 'UNIQUE', 'LA GRANGE', 'KY', 'PRIMARY', '38.4', '-85.37', 'NA-US-KY-LA GRANGE', 'FALSE', '', '', '')
(40033, 'STANDARD', 'LEBANON', 'KY', 'PRIMARY', '37.56', '-85.25', 'NA-US-KY-LEBANON', 'FALSE', '5086', '9191', '144240446')
(40036, 'STANDARD', 'LOCKPORT', 'KY', 'PRIMARY', '38.43', '-84.98', 'NA-US-KY-LOCKPORT', 'FALSE', '', '', '')

3. Find the largest zipcode value in the zipcodes_one shard.

(47750,)

4. Find the smallest zipcode value in the zipcodes_two shard.

(38257,)
```