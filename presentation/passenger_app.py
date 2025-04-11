import tkinter as tk
from tkinter import ttk, messagebox
from database.db_connection import get_db
from business_logic.passenger_service import PassengerService

class PassengerApp(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Passenger Sign Up")
        self.passenger_service = PassengerService()
        self._create_signup_widgets()

    def _create_signup_widgets(self):
        ttk.Label(self, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.username_entry = ttk.Entry(self)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.password_entry = ttk.Entry(self, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="First Name:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.first_name_entry = ttk.Entry(self)
        self.first_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Last Name:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.last_name_entry = ttk.Entry(self)
        self.last_name_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Email:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.email_entry = ttk.Entry(self)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Phone:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.phone_entry = ttk.Entry(self)
        self.phone_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Passport Number:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.passport_number_entry = ttk.Entry(self)
        self.passport_number_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Date of Birth (YYYY-MM-DD):").grid(row=7, column=0, padx=5, pady=5, sticky="w")
        self.dob_entry = ttk.Entry(self)
        self.dob_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self, text="Nationality:").grid(row=8, column=0, padx=5, pady=5, sticky="w")
        self.nationality_entry = ttk.Entry(self)
        self.nationality_entry.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        sign_up_button = ttk.Button(self, text="Sign Up", command=self._sign_up_passenger)
        sign_up_button.grid(row=9, column=0, columnspan=2, pady=10)

        self.grid_columnconfigure(1, weight=1)

    def _sign_up_passenger(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        passport_number = self.passport_number_entry.get()
        dob = self.dob_entry.get()
        nationality = self.nationality_entry.get()

        if not all([username, password, first_name, last_name, email, phone, passport_number, dob, nationality]):
            messagebox.showerror("Error", "All fields are required for sign up.")
            return

        passenger_data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": phone,
            "passport_number": passport_number,
            "dob": dob,
            "nationality": nationality
        }

        db = next(get_db())
        try:
            passenger_id = self.passenger_service.sign_up_passenger(db,
                                                                    username,
                                                                    password,
                                                                    first_name,
                                                                    last_name,
                                                                    email,
                                                                    phone,
                                                                    passport_number,
                                                                    dob,
                                                                    nationality)
            if passenger_id:
                messagebox.showinfo("Success", f"Sign up successful! Your Passenger ID is: {passenger_id}. You can now log in.")
                self.destroy()
            else:
                messagebox.showerror("Error", "Sign up failed. Username might be taken.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during sign up: {e}")
            db.rollback()
        finally:
            db.close()