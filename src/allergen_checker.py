import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import fasttext
import pandas as pd
import os

# Get the current directory of the script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Paths for model, dataset, and image
model_path = os.path.join(current_dir, "../model/allergen_detection_model_combined (1).bin")
dataset_path = os.path.join(current_dir, "../datasets/substitution_map.csv")
bg_image_path = os.path.join(current_dir, "../images/background.jpg")

# Verify the background image exists
if not os.path.exists(bg_image_path):
    print(f"Background image not found at {bg_image_path}")
    messagebox.showerror("Error", f"Background image not found at {bg_image_path}")
    exit()

# Load the trained FastText model
model = fasttext.load_model(model_path)

# Load the substitution map from a CSV file
def load_substitution_map(csv_file):
    df = pd.read_csv(csv_file)
    return dict(zip(df['Allergen'].str.lower(), df['Substitute Food Item'].str.lower()))

substitution_map = load_substitution_map(dataset_path)

# Function to Predict Allergens and Suggest Substitutes
def predict_and_replace(ingredients):
    prediction = model.predict(ingredients.lower())
    allergen_label = prediction[0][0]

    if allergen_label == "__label__contains":
        detected_allergens = []
        substitutes = {}

        for allergen in substitution_map.keys():
            if allergen in ingredients.lower():
                detected_allergens.append(allergen)
                substitutes[allergen] = substitution_map[allergen]

        return detected_allergens, substitutes
    else:
        return [], {}

# Callback Function for Button Click
def on_predict_click():
    ingredients = input_text.get("1.0", tk.END).strip()
    if not ingredients:
        messagebox.showerror("Error", "Please enter ingredients!")
        return

    detected_allergens, substitutes = predict_and_replace(ingredients)

    result_window = tk.Toplevel(root)
    result_window.title("Prediction Results")
    result_window.configure(bg="black")

    # Detected Allergens Label
    tk.Label(
        result_window,
        text="Detected Allergens:",
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white"
    ).pack(pady=10)

    if detected_allergens:
        tk.Label(
            result_window,
            text=", ".join(detected_allergens),
            font=("Arial", 12),
            bg="black",
            fg="white"
        ).pack(pady=5)
    else:
        tk.Label(
            result_window,
            text="No allergens detected.",
            font=("Arial", 12),
            bg="black",
            fg="white"
        ).pack(pady=5)

    # Suggested Substitutes Label
    tk.Label(
        result_window,
        text="Suggested Substitutes:",
        font=("Arial", 14, "bold"),
        bg="black",
        fg="white"
    ).pack(pady=10)

    if substitutes:
        substitute_text = "\n".join([f"{key} -> {value}" for key, value in substitutes.items()])
        tk.Label(
            result_window,
            text=substitute_text,
            font=("Arial", 12),
            bg="black",
            fg="white"
        ).pack(pady=5)
    else:
        tk.Label(
            result_window,
            text="No substitutes needed.",
            font=("Arial", 12),
            bg="black",
            fg="white"
        ).pack(pady=5)

# Create the Main Window
root = tk.Tk()
root.title("Allergen Checker")
root.geometry("500x400")

# Add Background Image
bg_image = Image.open(bg_image_path)
bg_image = bg_image.resize((500, 400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

# Create Canvas for Background
canvas = tk.Canvas(root, width=500, height=400)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Create GUI Components with Rounded Edges
def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=20, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Rounded Background for Title
create_rounded_rectangle(canvas, 150, 35, 350, 65, radius=15, fill="#EDF2F7", outline="")
title_label = tk.Label(root, text="Allergen Checker", font=("Arial", 20, "bold"), fg="#4A5568", bg="#EDF2F7")
canvas.create_window(250, 50, window=title_label)

# Rounded Background for Input
create_rounded_rectangle(canvas, 120, 150, 380, 190, radius=15, fill="#EDF2F7", outline="")
input_text = tk.Text(root, height=2, width=25, font=("Arial", 12), bg="#EDF2F7", fg="#2D3748", bd=0, highlightthickness=0)
canvas.create_window(250, 170, window=input_text)

# Rounded Button
create_rounded_rectangle(canvas, 180, 260, 320, 300, radius=20, fill="#4299E1", outline="")
predict_button = tk.Button(root, text="Check Allergens", command=on_predict_click, font=("Arial", 12), bg="#4299E1", fg="black", bd=0)
canvas.create_window(250, 280, window=predict_button)

# Run the Main Event Loop
root.mainloop()
