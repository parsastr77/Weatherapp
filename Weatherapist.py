# weatherapist app

import tkinter as tk
from tkinter import messagebox
from urllib.request import urlopen
from urllib.parse import quote
import json
import base64

app = tk.Tk()

def get_temp_city(event=None):
    city = ent.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city or country! ")
        return

    try:
        encoded_city = quote(city)
        url1 = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en"
        with urlopen(url1) as response:
            data = response.read().decode("utf-8")
            data = json.loads(data)
            if 'results' not in data or len(data['results']) == 0:
                raise ValueError("CityNotFound")
            location = data['results'][0]
            lat = location['latitude']
            long = location['longitude']

        url2 = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        with urlopen(url2) as response2:
            data2 = response2.read().decode("utf-8")
            data2 = json.loads(data2)
            current = data2["current"]

        lab3.config(
            text=f"last city entered: {city}"
        )
        lab.config(
            text=f"temprature: {current['temperature_2m']} °C\nwind speed: {current['wind_speed_10m']}"
        )

    except ValueError as e:
        if str(e) == "CityNotFound":
            messagebox.showerror("Error", f"{city} could not be found!")
        else:
            messagebox.showerror("Error", f"an error occured while sending request to thr server: {e}")
    except Exception as e:
        messagebox.showerror("Error", f"failed to connect to the server: {e}")

app.bind('<Return>', get_temp_city)


app.minsize(500,600)
app.resizable(False,False)
app.config(bg="#000000")
app.title("Open Weather")

ent = tk.Entry(
    master=app,
    bg="#9929EA",
    fg="#FAEB92",
    font=["Bebas Neue", 21],
    width=30,
    border=4
)
ent.place(x=80,y=300)

btn = tk.Button(
    master=app,
    text="Enter",
    bg="#CC66DA",
    fg="#FAEB92",
    font=["Bebas Neue", 16],
    width=20,
    height=2,
    command=get_temp_city
    ).place(x=160,y=410)

lab = tk.Label(
    master=app,
    text="",
    font=["Bebas Neue", 24],
    bg="black",
    fg="white"
)
lab.place(x=130,y=150)

lab2 = tk.Label(
    master=app,
    text="weatherapist",
    font=["Bebas Neue", 65],
    bg="black",
    fg="#FAEB92"
)
lab2.place(x=50,y=15)

lab3 = tk.Label(
    master=app,
    text=f"last city entered:",
    font=["Bebas Neue", 17],
    bg="black",
    fg="#73027D"
    )   
lab3.place(x=80,y=350)


app.mainloop()
