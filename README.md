docker-compose build
docker-compose up -d
docker-compose run backend python manage.py makemigrations
docker-compose run backend python manage.py migrate
docker-compose exec db psql --username=adrift
docker-compose run backend python manage.py createsuperuser

up = start containers from docker-compose.yml
run = start container & run command
exec = run command


-- Kafka --
1. It's similar to message broker (RabbitMQ) but it's designed for larger streams of data.
2. It's composed of Topic, Partitions, Producer and Consumer.
2.1 Topic can contain multiple partitions, allowing horizontal scaling and parallelism read, which can be spreaded across multiple brokers for better availability and performance.
2.2 Consumer are usually designed to run perpetually to detect any data coming. Use thread for this or else it will block the main process.
3. Consumer can contain group which dictate which consumers belong to which group.
4. value_serializer is important or else the sending/consume feature will not work.
5. INSIDE in the docker env is for the services within docker, and OUTSIDE is vice versa.
6. Duplication is bound to happen in kafka. Best way I thought of as of now will be just remove the duplicate in the transformation layers. Save those data in mongodb.
7. Remember to create the topic first or else producer sending process will get stuck.


-- Network --
1. When two devices across networks never spoke before, they require MAC address to communicate, the first initial request would be to retrieve that, known as ARP request, basically send a broadcast to that specific subnet of the ip to know who has this specific IP, tell me ur MAC address.
2. This is why `arp -a` command doesn't show the vm ip/mac address initially until a ping was done.
3. Without arp record, the initial ping to the specific ip address will actually be through the broadcast.