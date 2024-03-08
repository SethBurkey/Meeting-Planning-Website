                    ██████        ██████████  ██████████        ██████                  
                  ████        ███████████████████████████████        ████                
                  ████    ██████/ MEETING PLANNING WEBSITE \█████    ████                
                  ██████████████|         Made by          |███████████                
                    ████████████\______StacheOverflow™_____/█████████                  
                      ██████████████████          ██████████████████                    
                          ████████                      ████████ 

This project is a Proof-of-Concept design for a Meeting Planning Website.
The project was proposed by Greg Slade from frontiers.org with the intent of a web application that can
automate and optimize the planning process of finding a single meeting location for several missionaries 
from various locations around the world.

Created by Jacob Bender, Seth Burkey, and Ethan Hunter

SETUP:

**SERVER CONFIGURATION**
  *This project is intended to run on an Apache web server -- other considerations may be needed in order 
  to run on a different service.*
  -Apache servers do not run python scripts by default -- the server must be configured to run python/cgi
  -If not renamed, the server should be set up with /var/www/html/index.html as the main file

**API DAEMONS**
  In the the server's cron table (accessed with 'crontab -e') the following lines are used to periodically
  call the API, providing updated/'live' data:
    0 0 * * * /usr/bin/python3 /var/www/html/API/hotelAPI.py -t
    0 0 * * * /usr/bin/python3 /var/www/html/API/flightAPI.py PAR
  To achieve full production, the -t flag should be removed from hotelAPI.py and the flightAPI daemon
  should eventually be completely removed so that flightAPI.py can be called with the desired flight
  origin locations as arguments.

FUTURE DEVELOPMENT:
  The main area for the improvement of this project will come from upgrading the API. This will allow for
  more comprehensive data, giving a better approximation for the cost of meeting. This will also allow 
  for the UI to be expanded to include more options such as:
    -A toggle for willingness to have a roommate. This can cut down on the number of rooms needed


