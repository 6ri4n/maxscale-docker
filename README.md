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

## MaxScale Docker-Compose Setup

The [MaxScale docker-compose](./maxscale/docker-compose.yml) setup contains MaxScale
configured with a three node primary-replica cluster. 

**BEFORE PROCEEDING**: The following commands assume the user is in the docker group, if not, use "**sudo**" before each command.

The following commands should be executed within [this directory](./maxscale/):

Starting MaxScale with its primary-replica cluster:
```
docker-compose up -d
```

Viewing the status of the cluster:
```
$ docker-compose exec maxscale maxctrl list servers
┌─────────┬──────────┬──────┬─────────────┬─────────────────┬──────────┬─────────────────┐
│ Server  │ Address  │ Port │ Connections │ State           │ GTID     │ Monitor         │
├─────────┼──────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server1 │ primary  │ 3306 │ 0           │ Master, Running │ 0-3000-5 │ MariaDB-Monitor │
├─────────┼──────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server2 │ replica1 │ 3306 │ 0           │ Slave, Running  │ 0-3000-5 │ MariaDB-Monitor │
├─────────┼──────────┼──────┼─────────────┼─────────────────┼──────────┼─────────────────┤
│ server3 │ replica2 │ 3306 │ 0           │ Slave, Running  │ 0-3000-5 │ MariaDB-Monitor │
└─────────┴──────────┴──────┴─────────────┴─────────────────┴──────────┴─────────────────┘
```

Removing MaxScale and its cluster containers:
```
docker-compose down -v
```

## Running

**BEFORE PROCEEDING**: Everything in the [Configuration](https://github.com/6ri4n/maxscale-docker#configuration) section must have been completed.

The purpose of the Python script is to interact with and query the sharded database created using Docker Compose.

The following command should be executed within [this directory](./maxscale/):

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