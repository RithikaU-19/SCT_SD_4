import requests
from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import messagebox

def scrape_and_save():
    url = entry_url.get()
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        products = soup.find_all("article", class_="product_pod")

        with open("products.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Product Name", "Price", "Rating"])
            for product in products:
                name = product.h3.a["title"]
                price = product.find("p", class_="price_color").text.strip()
                rating_class = product.p.get("class", [])
                rating = rating_class[1] if len(rating_class) > 1 else "No rating"
                writer.writerow([name, price, rating])
        messagebox.showinfo("Success", "Data saved to products.csv")
    except Exception as e:
        messagebox.showerror("Error", str(e))

app = tk.Tk()
app.title("Product Scraper")

label = tk.Label(app, text="Enter e-commerce URL:")
label.pack(pady=5)

entry_url = tk.Entry(app, width=50)
entry_url.insert(0, "http://books.toscrape.com/")
entry_url.pack(pady=5)

scrape_button = tk.Button(app, text="Scrape and Save to CSV", command=scrape_and_save)
scrape_button.pack(pady=10)

app.mainloop()
