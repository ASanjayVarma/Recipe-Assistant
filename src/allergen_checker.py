import tkinter as tk
from tkinter import messagebox
import fasttext
import pandas as pd
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Paths for model and dataset
model_path = os.path.join(current_dir, "../model/allergen_detection_model_combined (1).bin")
dataset_path = os.path.join(current_dir, "../datasets/substitution_map.csv")

# Load the trained FastText model
model = fasttext.load_model(model_path)

# Load the substitution map from a CSV file
def load_substitution_map(csv_file):
    df = pd.read_csv(csv_file)
    return dict(zip(df['Allergen'].str.lower(), df['Substitute Food Item'].str.lower()))

substitution_map = load_substitution_map(dataset_path)

# Function to Predict Allergens and Suggest Substitutes
def predict_and_replace(ingredients):
    # Predict allergens using the FastText model
    prediction = model.predict(ingredients.lower())
    print(f"Prediction Output: {prediction}")  # Debugging output

    allergen_label = prediction[0][0]

    if allergen_label == "__label__contains":
        # Detect specific allergens
        detected_allergens = []
        substitutes = {}

        # Match allergens with substitution map
        for allergen in substitution_map.keys():
            if allergen in ingredients.lower():
                detected_allergens.append(allergen)
                substitutes[allergen] = substitution_map[allergen]

        print(f"Detected Allergens: {detected_allergens}")  # Debugging output
        print(f"Substitutes: {substitutes}")  # Debugging output
        return detected_allergens, substitutes
    else:
        print("No allergens detected")  # Debugging output
        return [], {}

# Callback Function for Button Click
def on_predict_click():
    ingredients = input_text.get("1.0", tk.END).strip()  # Get user input from text area
    if not ingredients:
        messagebox.showerror("Error", "Please enter ingredients!")
        return

    # Get predictions and substitutes
    detected_allergens, substitutes = predict_and_replace(ingredients)

    # Display results in a new window
    result_window = tk.Toplevel(root)
    result_window.title("Prediction Results")

    tk.Label(result_window, text="Detected Allergens:", font=("Arial", 14, "bold")).pack(pady=10)
    if detected_allergens:
        tk.Label(result_window, text=", ".join(detected_allergens), font=("Arial", 12)).pack(pady=5)
    else:
        tk.Label(result_window, text="No allergens detected.", font=("Arial", 12)).pack(pady=5)

    tk.Label(result_window, text="Suggested Substitutes:", font=("Arial", 14, "bold")).pack(pady=10)
    if substitutes:
        substitute_text = "\n".join([f"{key} -> {value}" for key, value in substitutes.items()])
        tk.Label(result_window, text=substitute_text, font=("Arial", 12)).pack(pady=5)
    else:
        tk.Label(result_window, text="No substitutes needed.", font=("Arial", 12)).pack(pady=5)

# Create the Main Window
root = tk.Tk()
root.title("Allergen Checker")

# Create GUI Components
title_label = tk.Label(root, text="Allergen Checker", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

input_label = tk.Label(root, text="Enter Ingredients (comma-separated):", font=("Arial", 12))
input_label.pack(pady=5)

input_text = tk.Text(root, height=5, width=40, font=("Arial", 12))
input_text.pack(pady=5)

predict_button = tk.Button(root, text="Check Allergens", command=on_predict_click, font=("Arial", 12))
predict_button.pack(pady=10)

# Run the Main Event Loop
root.mainloop()
