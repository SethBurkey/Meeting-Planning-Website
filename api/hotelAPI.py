'''
This file uses the Amadeus Hotel Search API (https://developers.amadeus.com/self-service/category/hotels/api-doc/hotel-search) 
to get the name, location, and price of hotels.
The API does not really fit what we need, but is the only one that has is somewhat free.

The paid version of the Amadeus API should work well, but it would require an additional step
where you query the Hotel List API (https://developers.amadeus.com/self-service/category/hotels/api-doc/hotel-list)
searching by city or geocode to obtain hotelIds. Then you can actually use hotelIds to query the Hotel Search API
to get useful data.
'''
import urllib.parse
import urllib.request
import json
import sqlite3

# Set up database connection + schema
connection = sqlite3.connect('hotelDB.db')
cursor = connection.cursor()
# cursor.execute('DROP TABLE IF EXISTS hotels') # Uncomment to delete table -> rebuild
cursor.execute('''CREATE TABLE IF NOT EXISTS hotels
                (id INTEGER PRIMARY KEY, 
                 name TEXT, 
                 location TEXT,
                 price TEXT)''')
# cursor.execute("DELETE FROM hotels") # Uncomment to clean table content

# Set up API connection to Amadeus
url = 'https://test.api.amadeus.com/v3/shopping/hotel-offers'

# Define query parameters
hotelID = 'MCLONGHM' # This needs to be retrieved from the search API, but is behind a paywall
check_in_date = '2024-03-05' # Get this from user # May need to be updated for this example to work
check_out_date = '2024-03-06'  # Get this from user # May need to be updated for this example to work
room_quantity = 1  # Get this from user
params = {
    'hotelIds': hotelID,
    'checkInDate': check_in_date,
    'checkOutDate': check_out_date,
    'roomQuantity': room_quantity
}

# Encode the query parameters
encoded_params = urllib.parse.urlencode(params)
full_url = url + '?' + encoded_params

# Automate access token generation
api_key = 'Qjx8b5xAw00UBm13k0sEXXm7KAS5rA0q' # This is given when Amadeus account is created
api_secret = 'JeOceGDwTOuie3Ho' # This is given when Amadeus account is created
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
        for hotel_offer in json_data['data']:
            hotel_name = hotel_offer['hotel']['name']
            hotel_location = hotel_offer['hotel']['cityCode']
            hotel_price = hotel_offer['offers'][0]['price']['total']

            # Insert into database
            cursor.execute("INSERT INTO hotels (name, location, price) VALUES (?, ?, ?)", (hotel_name, hotel_location, hotel_price))
            connection.commit()
            #''' DEBUGGING
            print("Name:", hotel_name)
            print("Location:", hotel_location)
            print("Price:", hotel_price)
            print()
            #'''
except urllib.error.HTTPError as e:
    # Handle HTTP errors
    print('HTTPError:', e.code, e.reason)
except urllib.error.URLError as e:
    # Handle URL errors
    print('URLError:', e.reason)

connection.close()
