import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from datetime import datetime

# Assuming data is defined somewhere
# ... (Your existing data loading and model training code)

data = pickle.load(open('preprocessed_data.pickle', mode='rb'))

def month_year(x, y):
    result_array = np.array([[str(i), x, y] for i in range(1, 31)])
    result_array_reshaped = result_array.reshape(-1, 3)
    return result_array_reshaped

class PredictionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Prediction App")
        self.master.iconbitmap("icon.ico") 

        # Add a logo and company name
        self.logo = tk.PhotoImage(file="mahaweli-authority.png")  # Replace with the actual path to your logo image
        #self.company_label = ttk.Label(master, text="Mahaweli Authority Sri Lanka", font=('Arial', 16, 'bold'))
        self.slogan_label = ttk.Label(master, text="Let's predict whether the spillway will open or not", font=('Arial', 12, 'italic'))
        self.logo_label = ttk.Label(master, image=self.logo)
        
        # Create and set up widgets
        self.label_month = ttk.Label(master, text="Month:")
        self.entry_month = ttk.Entry(master)
        self.label_year = ttk.Label(master, text="Year:")
        self.entry_year = ttk.Entry(master)
        self.predict_button = ttk.Button(master, text="Predict", command=self.make_prediction)

        # Layout
        #self.company_label.grid(row=0, column=3, columnspan=2, pady=10)
        self.logo_label.grid(row=0, column=1, columnspan=2, pady=10)
        self.slogan_label.grid(row=1, column=1, columnspan=2, pady=0, padx=10)  # Adjust pady as needed
        self.label_month.grid(row=2, column=1, padx=10, pady=10)
        self.entry_month.grid(row=2, column=2, padx=10, pady=10)
        self.label_year.grid(row=3, column=1, padx=10, pady=10)
        self.entry_year.grid(row=3, column=2, padx=10, pady=10)
        self.predict_button.grid(row=4, column=1, columnspan=2, pady=10)
        
    def make_prediction(self):
        try:
            month_value = int(self.entry_month.get())
            year_value = int(self.entry_year.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric values for Month and Year.")
            return
        

        month_data = month_year(month_value, year_value)

        try:
            prediction = clf.predict(month_data)

            tolerance = 1e-6  # You can adjust this based on your specific case
            
            if prediction is not None and np.any(np.abs(prediction) > tolerance):
                prediction_result = "opened"
            else:
                prediction_result = "closed"
            messagebox.showinfo("Prediction", f"The spillway will be {prediction_result}")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

if __name__ == "__main__":
    # Create and train your model (Assuming data is defined)
    X = data[['Day', 'Month', 'Year']]
    y = data['Cluster']
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.2)
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)

    # Create the main application window
    root = tk.Tk()
    app = PredictionApp(root)
    root.mainloop()
