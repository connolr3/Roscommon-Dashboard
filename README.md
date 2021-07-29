# Roscommon-Dashboard
Prepared By: Rose Connolly, April 2021 part of assignment in STU33001 Software Application module at TCD.
Run script_dashboard.py and visit http://127.0.0.1:8050/ in your browser to view the dashboard.
Some modules may have to be installed.
A dashboard was created using DASH in python. The figures created using PLOTLY.

Dashboard depenedent on file urls being maintained (if changed email for actual files to run)



Python Script
ROSCOMMON AREA AMENITIES - HERITAGE, SPORTS & BURIAL GROUNDS
Some modules may have to be downloaded before running script.

Choosing the Datasets
The datasets chosen are surveys of the available amenities in Roscommon as well as surrounding areas. The first dataset surveyed thatch buildings. The second dataset surveyed different burial grounds, but for our dashboard only graveyards were considered. The third dataset surveyed sports facilities such as GAA clubs or swimming pools.

The datasets were merged based on their town name. 

DATASET NAMES - AVAILABLE FROM DATA.GOV.IE, OR FOLLOW LINK IN PYTHON SCRIPT
Roscommon Thatch Building Survey
Roscommon Graveyard Survey 2005
Roscommon Sports Facilities


Cleaning and Manipulation

Town Names
Different surveys had used different spellings of town names e.g. ‘Balintibber’ vs ‘Ballintober’
Or defined areas differently e.g. ‘Kiltoom & Cam’ V ‘Kiltoom’
This meant a lot of Googling. Some smaller villages were combined as they all fall into a popular tourist walkway “Suck Valley Way”.
Fixing these areas meant creating an excel file in Python to display all the town names from each dataset for easy comparison.
The Sports Facility dataset did not define Town Name explicitly, and so a function had to be created in Python to extract this from the full address.

Sports Facility Type
There were a few sports facilities such as ‘Motor Club’ or ‘Boxing’ which were combined into an ‘Other’ section.

Geographic Coordinate System
One dataset used ITM (Irish Transverse Mercator) while the other two used Longitude and Latitude. 
For these datasets to be plotted on the same scale in the dashboard, the ITM scale had to be converted using a function.

Column Names
Corresponding data was named differently by each dataset e.g. ‘WebsiteLink’ vs ‘web’ or ‘Town’ V ‘Parish’.
Column names were changed where necessary to allow for a successful merge.




Dashboard
For the visualisation dropdown for cottages, the url had to be taken from the dataframe. Pandas default column width is 50 chars, and most urls were 58. The default column width had to be reset to 100.It took some time to track down this error. We saved the data as various csv files at different locations in the script. The URLs were perfect in the csv file. When searching for the image however, the URL would be shortened to 
It would have been nice to underlay a map or Roscommon under the scatterplot. This can be done with a scatter_geo plot however, this would have been difficult as most there is less functionality available for small countries like Ireland. Our coordinates were also in ITM, not longitude and latitude - there is no option to use ITM points, but this could have been solved in more time.


Main Difficulties
It was challenging finding a dataset with variables allowing for interesting comparison. The initial goal was to collect 3 datasets on facilities that would be appealing for tourists, however datasets such as Playgrounds and Angling spots had only 4 or so rows and would not be suitable for data display. There was a tourist attraction dataset however at least half of the rows were messed up beyond repair. We ended up analysing graveyards which is not as fun for tourists.
A lot of the data.gov.ie datasets had outdated urls.
It was unexpected the amount of time spent preparing the data to be merged.
It also took a while to get the layout of Dash dashboard correct i.e. number of rows and columns. The div components were tricky to place.


Further Work: convert coordinates in df to longitude/lattitude instead of ITM coords
Use these to build a geo scatter pliot that will display a map, instead of just a plain old scatter plt






