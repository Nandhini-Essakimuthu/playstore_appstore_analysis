# Importing the CSV reader module
from csv import reader
import matplotlib.pyplot as plt

# Open the CSV file for Google Play Store data
with open('googleplaystore.csv', 'r', encoding='utf-8') as file:
    # Create a CSV reader object
    csv_reader = reader(file)
    
    # Read the header
    android_header = next(csv_reader)
    
    # Read the rest of the data
    android = list(csv_reader)

# Open the CSV file for Apple App Store data
with open('AppleStore.csv', 'r', encoding='utf-8') as file:
    # Create a CSV reader object
    csv_reader = reader(file)
    
    # Read the header
    ios_header = next(csv_reader)
    
    # Read the rest of the data
    ios_data = list(csv_reader)

# Define a function to explore the dataset
def explore_data(dataset, start, end, count_rows_column=False):
    for i in dataset[start:end]:
        print(i)
        print('\n')
    if count_rows_column:
        print("number of rows", len(dataset))
        print("number of columns", len(dataset[0]))

# Print the header and explore the Google Play Store dataset
print(android_header)
print("\n")
explore_data(android, 540, 544, count_rows_column=True)

# Print the header and explore the Apple App Store dataset
print(ios_header)
print("\n")
explore_data(ios_data, 540, 544, count_rows_column=True)

# Identify duplicate apps in the Google Play Store dataset
unique_apps = []
duplicate_apps = []
for row in android:
    name = row[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

# Print the number of unique and duplicate apps in the Google Play Store dataset
print("number of unique apps", len(unique_apps))
print("number of duplicate apps", len(duplicate_apps))

# Function to convert the number of reviews to a common scale (e.g., million)
def convert_million(s):
    if s.endswith('M'):
        s = s.rstrip('M')
        return float(s) * 1000000
    else:
        return float(s)

# Identify the maximum number of reviews for each app in the Google Play Store dataset
reviews_max = {}
for row in android:
    name = row[0]
    n_review = convert_million(row[3])
    if name in reviews_max and reviews_max[name] < n_review:
        reviews_max[name] = n_review
    elif name not in reviews_max:
        reviews_max[name] = n_review

# Create a clean dataset with unique apps and maximum reviews
android_clean = []
already_added = []
for row in android:
    name = row[0]
    n_review = convert_million(row[3])
    if n_review == reviews_max[name] and name not in already_added:
        android_clean.append(row)
        already_added.append(name)

# Print the length of the clean Google Play Store dataset
print(len(android_clean))

# Identify duplicate apps in the Apple App Store dataset
unique_apps = []
duplicate_apps = []
for row in ios_data:
    name = row[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)

# Print the number of unique and duplicate apps in the Apple App Store dataset
print("number of unique apps", len(unique_apps))
print("number of duplicate apps", len(duplicate_apps))

# Function to check if the app name is in English
def check_eng(name):
    non_ascii = 0
    for ch in name:
        if ord(ch) > 127:
            non_ascii += 1
    if non_ascii > 3:
        return False
    else:
        return True

# Filter English apps from the Google Play Store dataset
android_english = []
for row in android_clean:
    name = row[0]
    if check_eng(name):
        android_english.append(row)

# Print the length of the English Google Play Store dataset
print(len(android_english))

# Filter English apps from the Apple App Store dataset (Commented out to focus on Android analysis)
# ios_english = []
# for row in ios_data:
#     name = row[0]
#     if check_eng(name):
#         ios_english.append(row)
# print(len(ios_english))

# Further filter free apps from the Google Play Store dataset
android_final = []
for row in android_english:
    price = row[7]
    if price == '0':
        android_final.append(row)

# Further filter free apps from the Apple App Store dataset
ios_final = []
for row in ios_data:
    price = row[4]
    if price == '0.0':
        ios_final.append(row)

# Print the length of the final Google Play Store and Apple App Store datasets
print(len(android_final))
print(len(ios_final))

# Function to create a frequency table for a specified column
def freq_table(dataset, index):
    freq_dict = {}
    total = 0
    for row in dataset:
        total += 1
        genre = row[index]
        if genre in freq_dict:
            freq_dict[genre] += 1
        else:
            freq_dict[genre] = 1
    freq_dict_prec = {}
    for key in freq_dict:
        percentage = freq_dict[key] / total * 100
        freq_dict_prec[key] = percentage
    return freq_dict_prec

# Print frequency tables for genres/categories in the Apple App Store and Google Play Store datasets
print(freq_table(ios_final, -5))
print(freq_table(android_final, 1))

# Create a frequency table for genres in the Apple App Store dataset
ios_genres = freq_table(ios_final, -5)

# Calculate and print the average user ratings for each genre in the Apple App Store
for genre in ios_genres:
    total = 0
    len_genre = 0
    for key in ios_final:
        genre_app = key[-5]
        if genre_app == genre:
            n_rating = float(key[5])
            total += n_rating
            len_genre += 1
    average = total / len_genre
    print(genre, ' : ', average)

# Print the names and ratings of apps in the 'Food & Drink' category in the Apple App Store
for app in ios_final:
    if app[-5] == 'Food & Drink':
        print(app[1], ':', app[5])

# Create a frequency table for categories in the Google Play Store dataset
android_genres = freq_table(android_final, 1)

# Calculate and print the average number of installs for each category in the Google Play Store
for category in android_genres:
    total = 0
    len_category = 0
    for key in android_final:
        category_app = key[1]
        installs = key[5]
        installs = installs.replace(',', '')
        installs = installs.replace('+', '')
        installs = float(installs)
        total += installs
        len_category += 1
    average = total / len_category
    print(category, ':', average)
    
    # Print the names and number of installs for apps in the 'COMMUNICATION' category with large user bases
    for app in android_final:
        if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
            print(app[0], ':', app[5])

# Filter Google Play Store apps with installs under 100 million in the 'COMMUNICATION' category
under_100_m = []
for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))

# Calculate and print the average number of installs for apps under 100 million in the 'COMMUNICATION' category
average_under_100_m = sum(under_100_m) / len(under_100_m)
print(average_under_100_m)

# Print the names and number of installs for apps in the 'PHOTOGRAPHY' category in the Google Play Store
for app in android_final:
    if app[1] == 'PHOTOGRAPHY':
        print(app[0], ':', app[5])

# Print the names and number of installs for apps in the 'BOOKS_AND_REFERENCE' category in the Google Play Store
for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])

# Print the names and number of installs for highly installed apps in the 'BOOKS_AND_REFERENCE' category
for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])

# Print the names and number of installs for moderately installed apps in the 'BOOKS_AND_REFERENCE' category
for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])
plt.figure(figsize=(10, 6))
plt.bar(ios_genres.keys(), ios_genres.values())
plt.title('Frequency of Genres in Apple App Store')
plt.xlabel('Genres')
plt.ylabel('Percentage')
plt.xticks(rotation=45, ha='right')
plt.show()

# Plotting a bar chart for the frequency table of categories in the Google Play Store dataset
plt.figure(figsize=(10, 6))
plt.bar(android_genres.keys(), android_genres.values())
plt.title('Frequency of Categories in Google Play Store')
plt.xlabel('Categories')
plt.ylabel('Percentage')
plt.xticks(rotation=45, ha='right')
plt.show()

# Extract app ratings from the dataset
app_ratings = [float(app[2]) for app in android_final]

# Plot a histogram for app ratings
plt.figure(figsize=(10, 6))
plt.hist(app_ratings, bins=30, color='lightcoral', edgecolor='black')
plt.title('Distribution of App Ratings in Google Play Store')
plt.xlabel('App Rating')
plt.ylabel('Frequency')
plt.show()


# Extract app prices from the dataset
app_prices = [float(app[7].replace('$', '')) for app in android_final]

# Plot a histogram for app prices
plt.figure(figsize=(10, 6))
plt.hist(app_prices, bins=30, color='lightgreen', edgecolor='black')
plt.title('Distribution of App Prices in Google Play Store')
plt.xlabel('App Price (in $)')
plt.ylabel('Frequency')
plt.show()

# Extract app ratings from the dataset (for Apple App Store)
ios_app_ratings = [float(app[7]) for app in ios_final]

# Plot a histogram for app ratings (for Apple App Store)
plt.figure(figsize=(10, 6))
plt.hist(ios_app_ratings, bins=30, color='lightcoral', edgecolor='black')
plt.title('Distribution of App Ratings in Apple App Store')
plt.xlabel('App Rating')
plt.ylabel('Frequency')
plt.show()


# Extract app prices from the dataset (for Apple App Store)
ios_app_prices = [float(app[4]) for app in ios_final]

# Plot a histogram for app prices (for Apple App Store)
plt.figure(figsize=(10, 6))
plt.hist(ios_app_prices, bins=30, color='lightgreen', edgecolor='black')
plt.title('Distribution of App Prices in Apple App Store')
plt.xlabel('App Price (in $)')
plt.ylabel('Frequency')
plt.show()

# Create a dictionary to store the total prices and counts for each genre
genre_prices = {}
genre_counts = {}

# Iterate through the Apple App Store dataset
for app in ios_final:
    genre = app[-4]  # Assuming the genre is in the -4 index column
    price = float(app[4])  # Assuming the price is in the 4 index column
    if genre in genre_prices:
        genre_prices[genre] += price
        genre_counts[genre] += 1
    else:
        genre_prices[genre] = price
        genre_counts[genre] = 1

# Calculate the average price for each genre
genre_avg_prices = {genre: genre_prices[genre] / genre_counts[genre] for genre in genre_prices}

# Find the genre with the highest average price
most_expensive_genre = max(genre_avg_prices, key=genre_avg_prices.get)

print("The most expensive genre in the Apple App Store is:", most_expensive_genre)

# Find the app with the maximum rating in the Apple App Store dataset
max_rating_app = max(ios_final, key=lambda app: float(app[7]))

# Extract relevant information
app_name = max_rating_app[1]
max_rating = float(max_rating_app[7])

# Print the details
print(f"The app with the maximum rating in the Apple App Store is '{app_name}' with a rating of {max_rating} points.")

import matplotlib.pyplot as plt

# Create a dictionary to store average ratings for each genre
average_ratings_by_genre = {}

# Calculate average user ratings for each genre
for genre in ios_genres:
    total_ratings = 0
    num_apps = 0
    for app in ios_final:
        if app[-5] == genre and float(app[4]) == 0.0:
            total_ratings += float(app[5])
            num_apps += 1
    if num_apps > 0:
        average_ratings = total_ratings / num_apps
        average_ratings_by_genre[genre] = average_ratings

# Plot a bar chart for average user ratings of free apps by genre
plt.figure(figsize=(12, 8))
plt.bar(average_ratings_by_genre.keys(), average_ratings_by_genre.values(), color='skyblue')
plt.title('Average User Ratings for Free Apps by Genre (Apple App Store)')
plt.xlabel('Genre')
plt.ylabel('Average User Rating')
plt.xticks(rotation=45, ha='right')
plt.show()


# Create a dictionary to store average ratings for each category in the Google Play Store
average_ratings_by_category = {}

# Calculate average user ratings for each category
for category in android_genres:
    total_ratings = 0
    num_apps = 0
    for app in android_final:
        if app[1] == category and float(app[7]) == 0.0:
            total_ratings += float(app[2])
            num_apps += 1
    if num_apps > 0:
        average_ratings = total_ratings / num_apps
        average_ratings_by_category[category] = average_ratings

# Plot a bar chart for average user ratings of free apps by category
plt.figure(figsize=(12, 8))
plt.bar(average_ratings_by_category.keys(), average_ratings_by_category.values(), color='lightcoral')
plt.title('Average User Ratings for Free Apps by Category (Google Play Store)')
plt.xlabel('Category')
plt.ylabel('Average User Rating')
plt.xticks(rotation=45, ha='right')
plt.show()
