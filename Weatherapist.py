# weatherapist app

import tkinter as tk
from tkinter import messagebox
from urllib.request import urlopen, Request
from urllib.parse import quote
import json

app = tk.Tk()

def open_getlatlong():
    page_get_city = tk.Toplevel()

    page_get_city.minsize(500,600)
    page_get_city.resizable(False,False)
    page_get_city.config(bg="black")
    page_get_city.title("get lat/long")

    lab_result_lat_long = tk.Label(
    master=page_get_city,
    text="",
    font=["Bebas Neue", 24],
    bg="black",
    fg="white"
    )
    lab_result_lat_long.place(x=140,y=90)

    lab_weatherapist2 = tk.Label(
    master=page_get_city,
    text="city finder",
    font=["Bebas Neue", 35],
    bg="black",
    fg="#FAEB92"
    )
    lab_weatherapist2.place(x=150,y=9)

    ent_get_lat = tk.Entry(
    master=page_get_city,
    bg="#9929EA",
    fg="#FAEB92",
    font=["Bebas Neue", 17],
    width=30,
    border=4
    )
    ent_get_lat.place(x=110,y=240)

    ent_get_long = tk.Entry(
        master=page_get_city,
        bg="#9929EA",
        fg="#FAEB92",
        font=["Bebas Neue", 17],
        width=30,
        border=4
    )
    ent_get_long.place(x=110,y=290)

    btn_get_lat_long = tk.Button(
    master=page_get_city,
    text="Enter lat/long",
    bg="#CC66DA",
    fg="#FAEB92",
    font=["Bebas Neue", 16],
    width=20,
    height=1,
    command=lambda: get_lat_long(
        ent_get_lat,
        ent_get_long,
        lab_result_lat_long
        )
    )
    btn_get_lat_long.place(x=160,y=380)


def get_temp_city(event=None):
    city = ent.get().strip()
    if not city:
        messagebox.showerror("Error", "Please enter a city or country! ")
        return

    try:
        encoded_city = quote(city)
        url1 = f"https://geocoding-api.open-meteo.com/v1/search?name={encoded_city}&count=1&language=en"
        req1 = Request(
            url1,
            headers={"User-Agent": "Weatherapist/1.0"}
        )
        with urlopen(req1, timeout=10) as response:
            data = response.read().decode("utf-8")
            data = json.loads(data)
            if 'results' not in data or len(data['results']) == 0:
                raise ValueError("CityNotFound")
            location = data['results'][0]
            lat = location['latitude']
            long = location['longitude']

        url2 = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
        req2 = Request(
            url2,
            headers={"User-Agent": "Weatherapist/1.0"}
        )
        with urlopen(req2, timeout=10) as response2:
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

def get_lat_long(entlat, entlong, resulabel):
    if not entlat.get().strip() or not entlong.get().strip():
        messagebox.showerror("Error", "Please enter both coordinates!")
        return
    latit = float(entlat.get().strip())
    longit = float(entlong.get().strip())
    try:
        latit = float(entlat.get().strip())
        longit = float(entlong.get().strip())
        if not -90 <= latit <= 90:
            raise ValueError("Invalid latitude!")
        if not -180 <= longit <= 180:
            raise ValueError("Invalid longitude!")
        url1 = f"https://nominatim.openstreetmap.org/reverse?lat={latit}&lon={longit}&format=jsonv2&addressdetails=1&accept-language=en"
        req = Request(
                url1,
                headers={"User-Agent": "Weatherapist/1.0"}
            )
        with urlopen(req, timeout=10) as response:
            data3 = response.read().decode("utf-8")
            data3 = json.loads(data3)
            if 'address' not in data3 or len(data3['address']) == 0:
                    raise ValueError("CityNotFound")
            country = data3["address"]["country"]
            country_code = data3["address"]["country_code"]

        resulabel.config(
            text=f"country name: {country}\ncountry code: {country_code}"
        )

    except ValueError as f:
        if str(f) == "CityNotFound":
            messagebox.showerror("Error", "city could not be found!")
        else:
            messagebox.showerror("Error", f"an error occured while sending request to thr server: {f}")
    except Exception as f:
        messagebox.showerror("Error", f"failed to connect to the server: {f}")




app.minsize(500,600)
app.resizable(False,False)
app.config(bg="black")
app.title("Open Weather")

ent = tk.Entry(
    master=app,
    bg="#9929EA",
    fg="#FAEB92",
    font=["Bebas Neue", 21],
    width=30,
    border=4
)
ent.place(x=80,y=420)

btn = tk.Button(
    master=app,
    text="Enter city",
    bg="#CC66DA",
    fg="#FAEB92",
    font=["Bebas Neue", 16],
    width=20,
    height=1,
    command=get_temp_city
    )
btn.place(x=160,y=520)

btn2 = tk.Button(
    master=app,
    text="city finder",
    bg="#CC66DA",
    fg="#FAEB92",
    font=["Bebas Neue", 16],
    width=20,
    height=1,
    command=open_getlatlong
    )
btn2.place(x=160,y=200)


lab = tk.Label(
    master=app,
    text="",
    font=["Bebas Neue", 24],
    bg="black",
    fg="white"
)
lab.place(x=140,y=90)

lab_weatherapist1 = tk.Label(
    master=app,
    text="weatherapist",
    font=["Bebas Neue", 35],
    bg="black",
    fg="#FAEB92"
)
lab_weatherapist1.place(x=136,y=9)

lab3 = tk.Label(
    master=app,
    text=f"last city entered:",
    font=["Bebas Neue", 17],
    bg="black",
    fg="#73027D"
    )   
lab3.place(x=80,y=470)

lab4 = tk.Label(
    text="",
    font=["Bebas Neue", 24],
    bg="black",
    fg="white"
)
# lab.place(x=140,y=90)


app.mainloop()