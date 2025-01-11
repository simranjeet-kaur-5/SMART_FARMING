import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

# Define the dictionary with crop prices
crop_prices = {
    "Wheat": 33.0,  # Price in INR per kg
    "Rice": 20.0,   # Price in INR per kg
    "Corn": 25.0,   # Price in INR per kg
    "Sugarcane": 40.0,  # Price in INR per kg
    "Soybean": 70.0,  # Price in INR per kg
    "Cotton": 100.0,  # Price in INR per kg
    "Potato": 15.0,  # Price in INR per kg
    "Tomato": 20.0,  # Price in INR per kg
    "Banana": 25.0,  # Price in INR per kg
    "Apple": 150.0   # Price in INR per kg
}

# Function to get the price of the selected crop
def get_crop_price(crop_name):
    # Check if the crop is available in the dictionary
    if crop_name in crop_prices:
        return crop_prices[crop_name]
    else:
        return "Crop not found."

# Function to get pests for the selected crop and display images
def get_pests_for_crop(crop_name):
    pests_data = {
        "Wheat": ["Wheat Rust", "Wheat Stem Sawfly"],
        "Rice": ["Rice Weevil", "Brown Planthopper"],
        "Corn": ["Corn Borer", "Corn Rootworm"],
        "Sugarcane": ["Sugarcane Aphid", "Sugarcane Borer"],
        "Soybean": ["Soybean Aphid", "Soybean Cyst Nematode"],
        "Cotton": ["Cotton Bollworm", "Cotton Leafworm"],
        "Potato": ["Potato Beetle", "Late Blight"],
        "Tomato": ["Tomato Hornworm", "Whitefly"],
        "Banana": ["Banana Borer", "Banana Weevil"],
        "Apple": ["Codling Moth", "Aphid"]
    }

    if crop_name in pests_data:
        print(f"\nPotential pests for {crop_name}:")
        for pest in pests_data[crop_name]:
            print(f"- {pest}")
            # Display pest image
            image_url = get_pest_image_from_google(pest)
            if image_url:
                print(f"  Image URL: {image_url}")
                display_image(image_url)  # Display the pest image
    else:
        print(f"No pests found for {crop_name}.")

# Function to fetch pest images from Google Custom Search
def get_pest_image_from_google(pest_name):
    api_key = "AIzaSyA-Ml_os2XGlF2KAcH9MwhvaQZmGqR4nn4"  # Replace with your API key from Google Cloud Console
    cse_id = "b580ae8722ce34ef2"  # Replace with your Custom Search Engine ID

    url = f"https://www.googleapis.com/customsearch/v1?q={pest_name}&searchType=image&key={api_key}&cx={cse_id}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        if 'items' in data:
            image_url = data['items'][0]['link']
            return image_url
        else:
            print(f"No image found for {pest_name}.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching image for {pest_name}: {e}")
        return None

# Function to fetch weather data from OpenWeatherMap API
def get_weather(city_name, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        city = data['name']
        country = data['sys']['country']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        weather_description = data['weather'][0]['description']
        return city, country, temperature, humidity, weather_description
    except requests.exceptions.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None

# Function to fetch crop prices from AgriWatch
def fetch_crop_prices():
    url = 'https://www.agriwatch.com/'  # Main AgriWatch URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the price table (you may need to adjust this based on the actual page structure)
    prices = []
    table = soup.find('table', {'commodity': 'Average'})  # Example class, adjust based on the actual HTML
    if table:
        for row in table.find_all('tr')[1:]:  # Skip the header row
            columns = row.find_all('td')
            if len(columns) > 1:
                crop_name = columns[0].text.strip()  # Name of the crop
                crop_price = columns[1].text.strip()  # Price of the crop
                prices.append((crop_name, crop_price))

    return prices

# Fetch and display the prices
prices = fetch_crop_prices()
if prices:
    for crop, price in prices:
        print(f"Crop: {crop}, Price: {price}")
else:
    print("No prices found.")

# Function to display image from a URL
def display_image(image_url):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        img.show()  # This will open the image in the default image viewer
    except Exception as e:
        print(f"Error displaying image: {e}")

# Predefined list of crops and their recommendations
crops_data = [
    ("Wheat", "Loam", 5.5, 7.5, "Nitrogen Fertilizer"),
    ("Rice", "Clay", 4.5, 6.5, "Phosphorus Fertilizer"),
    ("Corn", "Sandy", 5.0, 7.0, "Potassium Fertilizer"),
    ("Sugarcane", "Alluvial", 6.0, 8.0, "Nitrogen Fertilizer"),
    ("Soybean", "Loam", 6.0, 7.5, "Organic Fertilizer"),
    ("Cotton", "Sandy Loam", 5.8, 8.0, "Phosphorus Fertilizer"),
    ("Potato", "Sandy Loam", 5.0, 6.5, "Compost Fertilizer"),
    ("Tomato", "Loamy Sand", 6.0, 6.8, "Organic Fertilizer"),
    ("Banana", "Clay Loam", 6.0, 7.5, "Nitrogen Fertilizer"),
    ("Apple", "Loam", 6.0, 7.0, "Potassium Fertilizer")
]

# Function to recommend crops and fertilizers based on user input and weather data
def recommend_crop_and_fertilizer(soil_type, ph, temperature, humidity):
    print(f"\nWeather Data: Temperature = {temperature}°C, Humidity = {humidity}%")
    print("\nRecommended crops based on your input:")

    found = False
    for crop in crops_data:
        crop_name, soil, min_ph, max_ph, fertilizer = crop

        if soil.lower() == soil_type.lower() and min_ph <= ph <= max_ph:
            found = True
            print(f"- {crop_name}")

            if temperature < 10:
                print(f"  Warning: Temperature too low for optimal growth of {crop_name}.")
            elif temperature > 30:
                print(f"  Warning: Temperature too high for optimal growth of {crop_name}.")

            if humidity < 40:
                print(f"  Warning: Humidity too low for {crop_name}.")
            elif humidity > 80:
                print(f"  Warning: Humidity too high for {crop_name}.")

            print(f"  Suitable Fertilizer: {fertilizer}")

            price = fetch_crop_prices()
            if price:
                print(f"  Real-time Market Price for {crop_name}: ${price}/unit")

    if not found:
        print("No crops found for the given soil type and pH range.")

# Main program
def main():
    print("Welcome to the Crop Recommendation and Fertilizer Suggestion System!")

    api_key = "2813da52abdbd908326a6228868796be"  # Replace with your OpenWeatherMap API key
    city_name = input("Enter your city name: ").strip()

    weather_data = get_weather(city_name, api_key)
    if weather_data:
        city, country, temperature, humidity, weather_description = weather_data
        print(f"\nWeather in {city}, {country}: {weather_description.capitalize()}")
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%")

        while True:
            print("\nEnter the following details for crop recommendation:")
            soil_type = input("Soil Type: ").strip()
            try:
                ph = float(input("pH Value: "))
            except ValueError:
                print("Invalid pH value. Please enter a numeric value.")
                continue

            recommend_crop_and_fertilizer(soil_type, ph, temperature, humidity)

            crop_selection = input("\nEnter the crop name from the recommendations to get pest information: ").strip()

            get_pests_for_crop(crop_selection)
            selected_crop = "Wheat"  # Replace with user input or selection
            price = get_crop_price(selected_crop)
            print(f"The price of {selected_crop} is {price} INR per kg.")
            cont = input("\nDo you want to search again? (yes/no): ").strip().lower()
            if cont != 'yes':
             print("Thank you for using the Crop Recommendation and Fertilizer Suggestion System!")
            break
    else:
        print("Could not retrieve weather data. Please try again later.")

if __name__ == "_main_":
    main()