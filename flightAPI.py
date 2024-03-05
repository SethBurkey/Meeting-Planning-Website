import urllib.parse
import urllib.request
import json
import sqlite3

# Set up database connection
connection = sqlite3.connect('flightDB.db')
cursor = connection.cursor()

# Set up API connection to Amadeus
url = 'https://test.api.amadeus.com/v1/shopping/flight-destinations'

# Define query parameters
# These can be determined based on data input into the UI
params = {
    'origin': 'PAR',
    'maxPrice': '200'
}

# Encode the query parameters
encoded_params = urllib.parse.urlencode(params)
full_url = url + '?' + encoded_params

# Automate access token generation
api_key = 'Qjx8b5xAw00UBm13k0sEXXm7KAS5rA0q' # This is given when Amadeus account is created
api_secret = 'JeOceGDwTOuie3Ho' # This is given when Amadeus account is created
access_token = 'ADjuxpMRDoAX1DqaVrdbCMWZ2sux' # This is retrieved from a JSON object returned when you send the api_key and api_secret to the token_url. This is the old one and is expired and doesnt really need tot be here
token_url = 'https://test.api.amadeus.com/v1/security/oauth2/token'
payload = {
    'grant_type': 'client_credentials',
    'client_id': api_key,
    'client_secret': api_secret
}
encoded_payload = urllib.parse.urlencode(payload).encode('utf-8')
token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
}
req = urllib.request.Request(token_url, data=encoded_payload, headers=token_headers, method='POST')

# Perform the request to get the token
try:
    with urllib.request.urlopen(req) as response:
        # Read the response data
        data = response.read().decode('utf-8')

        # Parse the JSON response
        token_data = json.loads(data)

        # Extract the access token from the response
        access_token = token_data.get('access_token')

        # Use the access token for subsequent API requests
        print("New Access Token:", access_token)
except urllib.error.HTTPError as e:
    # Handle HTTP errors
    print('HTTPError:', e.code, e.reason)
except urllib.error.URLError as e:
    # Handle URL errors
    print('URLError:', e.reason)



# Define headers with authorization
headers = {
    'Authorization': 'Bearer ' + access_token
}

# Create a request object
req = urllib.request.Request(full_url, headers=headers)

# Perform the GET request
try:
    with urllib.request.urlopen(req) as response:
        # Read the response data
        data = response.read().decode('utf-8')
        json_data = json.loads(data)
        # Extract relevent fields from response data
        for destination in json_data['data']:
            og_location = destination['origin']
            dst_location = destination['destination']
            ticket_price = destination['price']['total']
            depart_time = destination['departureDate']

            # Insert into database
            cursor.execute("INSERT INTO flights (origin_location, dest_location, price, departure_time) VALUES (?, ?, ?, ?)", (og_location, dst_location, ticket_price, depart_time))
            connection.commit()
            #''' DEBUGGING
            print("Origin:", og_location)
            print("Destination:", dst_location)
            print("Price:", ticket_price)
            print("Departure Date:", depart_time)
            # print("Arrival Time:", arrival_time)
            # print("Flight Duration:", flight_duration)
            print()
            #'''
except urllib.error.HTTPError as e:
    # Handle HTTP errors
    print('HTTPError:', e.code, e.reason)
except urllib.error.URLError as e:
    # Handle URL errors
    print('URLError:', e.reason)

connection.close()
