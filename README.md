## bus_route_api_consumption

Python script to find out how long until the next bus to arrive.

How to run the script

Clone the repository into local where python is installed. if not install python.

To run this code, it required three arguments to find out. run below command.

**% python3 bus_route.py --help**

usage: bus_route.py [-h] --bus-route BUS_ROUTE --bus-stop-name BUS_STOP_NAME --direction {east,west,north,south}

Provide information to get the wait time for the next bus.

optional arguments:

  -h, --help            show this help message and exit
  
  --bus-route BUS_ROUTE
  
                        BUS ROUTE
                        
  --bus-stop-name BUS_STOP_NAME
  
                        BUS STOP NAME
                        
  --direction {east,west,north,south}
  
                        Direction Of Travel
                        

To get the results, run as a below command by passing above required arguments. Result will be displyed in minutes remaining.


**% python3 bus_route.py --bus-route="METRO Blue line" --bus-stop-name="Target Field Station Platform 2" --direction="north"**

13 minutes

**% python3 bus_route.py --bus-route="Route 3" --bus-stop-name="Union Depot" --direction="east"**

32 minutes
