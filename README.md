# Smart Lego City
How to access the code
- Access the Rasberry PI (ssh pi@<ip_address (password is “nothing”)> 
- To sense and publish temperature and humidity
  - Git clone https://github.com/amjadmajid/OrchestraCity
  - Cd OrchestraCity
  - Python3 hotel_sensors.py
- To subscribe and save the sensory data in influx DB follow
  - Download and install [influxdb](https://docs.influxdata.com/influxdb/v2/install/)
  - Set the correct configurations in `hotel_server.py` and then run it with `Python3 hotel_server.py`
- To visualize the data configure a Grafana dashboard and connect it to influx DB
