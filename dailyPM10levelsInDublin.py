import requests #To get the files 
import json #To use for scraping through the API 
from tabulate import tabulate #To show the data in a table format 
import csv #To create a csv file with the data
import matplotlib.pyplot as plt #To create the charts 
import pandas as pd#To create the charts
import plotly.graph_objects as go#To create the charts.
import sqlite3#To create a database

pm10Url = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude=53.3472&longitude=-6.2592&hourly=pm10&forecast_days=1" #Creating the variable for the url of the page with Particulate Matter PM10 data

pm10Data = requests.get(pm10Url)#Getting the page data
parsed_pm10Data = pm10Data.json()#Parsing the data into json
pm10Hourly = parsed_pm10Data["hourly"] #Getting the info within the "hourly" element
dateTimeInfo = pm10Hourly["time"]#Getting the date and time info within the "pm10" element
date = dateTimeInfo[12].split("T")[0] #Getting the date only (splitting the dateAndTime in date and time where T is)
pm10 = pm10Hourly["pm10"]#Getting the pm10 levels info within the "pm10" element
pm10AtMidday = pm10[12] #Getting the levels of pm10 at midday

#Using the Tabulate library to show the data on screen
tableData = [["Date","pm10 levels at midday"], [date, pm10AtMidday]]
tabulateTable = tabulate(tableData,  headers = "firstrow") #Putting the list into a table
print(tabulateTable)#Printing the table on screen

with open("dailyPM10levelsInDublin.csv", "a", newline="") as file: #This creates a csv file to which the pm10 info will be appended
                                                           #for every day scheduled.
    writer =csv.writer(file)#Creating a writer object to write into the CSV file
    for row in tableData:#For each row in the table...
        writer.writerow(row)#...write a row of data
print("dailyPM10levelsInDublin.csv file updated successfully")

myDatabase = sqlite3.connect("dailyPM10levelsInDublin.db")#Creating the database to store the data
cursor = myDatabase.cursor() #Creating the cursor to go through the database
cursor.execute('''
    CREATE TABLE IF NOT EXISTS 
    dailyPM10levels (date TEXT, pm10 FLOAT) ''') #Creating the table if it doesn't exist already
for row in tableData[1:]:#For each row in the table... (I am starting at index 1 so as not to count the first row with the headers)
    cursor.execute('''
        INSERT INTO dailyPM10levels(date, pm10)
        values (:date, :pm10) ''',{
            "date": date,
            "pm10":pm10AtMidday}) #...insert all daily info in each column
    myDatabase.commit()#Saving the changes

cursor.execute( #Selecting the info about the date and pm10 levels from the database
    "SELECT date, pm10 FROM dailyPM10levels"
    )
pm10data = cursor.fetchall() #Storing all fetched database info in a variable

Dates = [] #Creating a list to store the Dates values
pm10Levels = [] #Creating a list to store the values of the PM10 levels

for row in pm10data: #For each row in the pm10data variable...
    Dates.append(row[0])#... append the date value (which is at index 0) to Dates ...
    pm10Levels.append(row[1]) #... and append the pm10 value (which is at index 1) to pm10Levels             
     
# Using Matplotlib to create a map 
plt.plot(Dates, pm10Levels, #Passing the two lists containing all values collected throughout the days
         marker = "o", #Customizing the plot chart
         color = "blue",
         linewidth = 0.7,
         linestyle = "--",
         markeredgecolor = "purple", 
         markeredgewidth = "1.5", 
         markerfacecolor = "pink",
         markersize = 6.0
         )
plt.xlabel("Dates", size = 4) #Putting the dates label in the x axis and customizing the font size
plt.ylabel("PM10 level", size = 10) #Putting the pm10 label in the y axis and customizing the font size
plt.title("PM10 levels in µg/m³ at midday (GMT) in Dublin", color = "Blue", size = 10) #Title of the chart and customizing the font size and color
plt.style.use("seaborn-v0_8")#Customizing the style. List of styles available at https://matplotlib.org/stable/users/explain/customizing.html
plt.grid(True) #Putting the grid as a background
plt.xticks(rotation = 30)#To make the labels of the dates fully readable I had to move them diagonally a little
plt.savefig("dailyPM10levelsInDublin.svg", format="svg")#Saving the chart as svg


#Creating another type of chart and saving it in png
Daily_Data ={"Dates": Dates, #Storing into Daily_Data all values for each list
             "PM10 levels": pm10Levels}
df = pd.DataFrame(data=Daily_Data) #Creating a dataframe with pandas, containing the data of Daily_Data
fig = go.Figure() #Creating a figure object and assigning it to a variable, in order to be able to manipulate and modify it.
                  #Guidance found on https://www.angela1c.com/projects/dash/plotly/
fig.add_trace(#Adding a bar trace for the pm10 levels
    go.Bar(
        x=df["Dates"],
        y=df["PM10 levels"],
        marker={"color": "darkseagreen"}, #To customize the bar color, I referred to https://stackoverflow.com/questions/61746001/plotly-how-to-specify-colors-for-a-group-using-go-bar
                                          #and to https://matplotlib.org/stable/gallery/color/named_colors.html
        name="PM10 levels in µg/m³ at midday (GMT)"
    ))
fig.update_layout(
    title=dict(text="PM10 levels in µg/m³ at midday (GMT) in Dublin", font=dict(size=15))#Creating and customizing the title    
    )

fig.show()#Opening a webbrowser to show the image
fig.write_image("dailyPM10levelsInDublin.png")#Saving the image as png.
myDatabase.close()#Closing the database connection
