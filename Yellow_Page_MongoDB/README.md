The Python script the script performs web scraping to gather data about pizzerias in San Francisco from the Yellow Pages website. It saves this data to both HTML files and a MongoDB database, and it enriches the information with geolocation data from an external API.

1. **Saving Search Results Page (`main1()`):** The script initiates a search on Yellow Pages for pizzerias in San Francisco, retrieves the search results page, and saves it as an HTML file named `sf_pizzeria_search_page.html`.

2. **Extracting Information from Search Results (`main2()`):** The script reads the saved search results page, iterates through the search results, and extracts details about each pizzeria.

3. **Saving Information to MongoDB (`main3()`):** The script further processes the extracted information from the search results and organizes it into lists. It then creates a Pandas DataFrame from these lists.

4. **Geolocation Data and Database Update (`main3()` continued):** The script uses an external API called Positionstack to obtain latitude and longitude data for each pizzeria's address. It makes requests to the API based on the pizzeria addresses and updates the MongoDB collection with the retrieved geolocation data, along with other information such as address, phone number, website, etc.

5. **Updating Restaurant Information (`main3()` continued):** Finally, the script updates the existing MongoDB records for each pizzeria with the additional information acquired, including address, phone number, website, longitude, and latitude.

Image source: https://www.theinfatuation.com/san-francisco/reviews/long-bridge-pizza-co
