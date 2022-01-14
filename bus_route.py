import argparse
from datetime import datetime
from requests.exceptions import HTTPError

import requests


def transitInfo(url, bus_route, stop_name, direction):
    data = {}
    return_response = {
        'data': data,
        'isValid': False
    }
    try:
        response = requests.get(f"{url}/Routes")
        response.raise_for_status()
        for resp in response.json():
            if resp['route_label'].lower() == bus_route.lower():
                routeCode = resp['route_id']
                data['route_id'] = resp['route_id']
                directionResponse = requests.get(f"{url}/Directions/{routeCode}")
                directionResponse.raise_for_status()
                for resp in directionResponse.json():
                    if direction.lower() in resp['direction_name'].lower():
                        directionID = resp['direction_id']
                        data['direction_id'] = resp['direction_id']
                        stopsResponse = requests.get(f"{url}/Stops/{routeCode}/{directionID}")
                        stopsResponse.raise_for_status()
                        for resp in stopsResponse.json():
                            if stop_name.lower() == resp['description'].lower():
                                data['place_code'] = resp['place_code']
                                return_response['isValid'] = True
                                return return_response

    except HTTPError as http_err:
        print(f'HTTP error: {http_err}')
        return return_response
    except Exception as err:
        print(f'Other error: {err}')
        return return_response


def main():
    parser = argparse.ArgumentParser(
        description="Provide information to get the wait time for the next bus."
    )
    parser.add_argument("--bus-route", type=str, help="BUS ROUTE", required=True)
    parser.add_argument("--bus-stop-name", type=str, help="BUS STOP NAME", required=True)
    parser.add_argument("--direction", type=str, choices=['east', 'west', 'north', 'south'], help="Direction of travel",
                        required=True)

    args = parser.parse_args()

    url = "https://svc.metrotransit.org/nextripv2"
    response = transitInfo(url=url, bus_route=args.bus_route, stop_name=args.bus_stop_name,
                           direction=args.direction)

    if response is None:
        print("Please check your input.")

    elif response['isValid']:
        nextTripResponse = requests.get(
            f"{url}/{response['data']['route_id']}/{response['data']['direction_id']}/{response['data']['place_code']}")
        departure_time = nextTripResponse.json()['departures'][0]['departure_text']
        if "Min" in departure_time:
            print(departure_time.replace("Min", "minutes"))
        else:
            now = datetime.now()
            current_time = now.strftime("%I:%M")
            timeDiff = datetime.strptime(str(departure_time), '%I:%M') - datetime.strptime(str(current_time), '%I:%M')
            print(f"{int(timeDiff.seconds / 60)} minutes")
    else:
        print("This is not a valid request.")


if __name__ == "__main__":
    main()
