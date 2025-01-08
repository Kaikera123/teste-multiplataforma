import requests
from bs4 import BeautifulSoup
import pandas as pd
import random
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Button, messagebox, Canvas

# Function to scrape lottery data
def scrape_lottery_results():
    print("Attempting to fetch lottery results...")
    url = "https://loteriaguru.com/brasil-resultados-loteria"
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Error accessing the site. Status code: {response.status_code}")
        messagebox.showerror("Error", "Failed to access lottery results.")
        return None

    print("Successfully connected to the site. Extracting data...")
    soup = BeautifulSoup(response.content, "html.parser")
    results = []

    # Select all <ul> elements with the class 'lg-numbers game-number'
    for ul in soup.select("ul.lg-numbers.game-number"):
        # Extract numbers from each <li> element
        numbers = [int(li.text.strip()) for li in ul.find_all("li", class_="lg-number")]
        results.append({"numbers": numbers})

    print(f"Extracted data: {results}")
    return results

# Function to analyze and plot data
def analyze_and_plot(data):
    all_numbers = [num for draw in data for num in draw['numbers']]
    number_counts = pd.Series(all_numbers).value_counts()

    plt.figure(figsize=(10, 6))
    number_counts.sort_index().plot(kind='bar', color='skyblue')
    plt.title("Frequency of Drawn Numbers")
    plt.xlabel("Numbers")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Function to suggest random numbers
def suggest_numbers(data):
    all_numbers = [num for draw in data for num in draw['numbers']]
    most_frequent = pd.Series(all_numbers).value_counts().index[:10].tolist()
    suggestion = random.sample(most_frequent, 6)
    messagebox.showinfo("Number Suggestion", f"Suggested numbers: {', '.join(map(str, suggestion))}")

# Main GUI setup
def main():
    # Scrape data initially
    lottery_data = scrape_lottery_results()
    if not lottery_data:
        return

    root = Tk()
    root.title("Lottery Analyzer")
    root.geometry("600x400")

    # Set up background color
    canvas = Canvas(root, width=600, height=400, bg="#d4f8e8")  # Light green background
    canvas.pack(fill="both", expand=True)

    # Add title label
    title_label = Label(root, text="Welcome to the Lottery Analyzer!", font=("Arial", 18, "bold"), bg="#d4f8e8", fg="#006400")  # Dark green text
    title_label_window = canvas.create_window(300, 50, window=title_label)

    # Add buttons with custom colors
    update_button = Button(root, text="Update Results", command=lambda: scrape_lottery_results(), bg="black", fg="white", font=("Arial", 12))
    view_button = Button(root, text="View Charts", command=lambda: analyze_and_plot(lottery_data), bg="black", fg="white", font=("Arial", 12))
    generate_button = Button(root, text="Generate Numbers", command=lambda: suggest_numbers(lottery_data), bg="black", fg="white", font=("Arial", 12))

    canvas.create_window(300, 150, window=update_button, width=200, height=40)
    canvas.create_window(300, 200, window=view_button, width=200, height=40)
    canvas.create_window(300, 250, window=generate_button, width=200, height=40)

    root.mainloop()

if __name__ == "__main__":
    print("Starting the program...")
    main()

