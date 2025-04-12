import tkinter as tk
from tkinter import ttk, messagebox
from business_logic.authentication_service import AuthenticationService
from business_logic.flight_service import FlightService
from business_logic.booking_service import BookingService
from presentation.aircraft_app import AircraftApp
from presentation.flight_app import FlightApp
from presentation.airline_app import AirlineApp
from presentation.report_app import ReportApp
from presentation.crew_app import CrewApp
from presentation.passenger_app import PassengerApp
from database.db_connection import get_db, init_db

class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Skyline Airways System - Login")
        self.geometry("500x500")
        init_db()
        self.resizable(False, False)
        self.auth_service = AuthenticationService()
        self.flight_service = FlightService()
        self.booking_service = BookingService()
        self.current_user_id = None
        self.current_user_role = None
        self.crew_app_instance = None
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self._create_login_widgets()

    def _create_login_widgets(self):
        ttk.Label(self, text="Username:").pack(pady=5)
        ttk.Entry(self, textvariable=self.username_var).pack(pady=5)

        ttk.Label(self, text="Password:").pack(pady=5)
        ttk.Entry(self, textvariable=self.password_var, show="*").pack(pady=5)

        login_button = ttk.Button(self, text="Login", command=self._login)
        login_button.pack(pady=10)

        signup_button = ttk.Button(self, text="Passenger Sign Up", command=self._show_passenger_signup)
        signup_button.pack(pady=10)

    def _login(self):
        username = self.username_var.get()
        password = self.password_var.get()
        db = next(get_db())
        try:
            user = self.auth_service.authenticate_user(db, username, password)
            if user:
                self.current_user_id = user.id
                self.current_user_role = user.role
                messagebox.showinfo("Login Successful", f"Logged in as: {user.role.capitalize()}")
                self._show_main_app()
            else:
                messagebox.showerror("Login Failed", "Invalid username or password.")
        finally:
            db.close()

    def _show_passenger_signup(self):
        passenger_app = PassengerApp(self)
        self.title("Register Passenger")
        passenger_app.grab_set()
        self.wait_window(passenger_app)

    def _show_main_app(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.title(f"Skyline Airways System - {self.current_user_role.capitalize()}")
        self.geometry("600x400")
        self.resizable(True, True)

        if self.current_user_role == "Admin":
            self._show_admin_options()
        elif self.current_user_role in ("Pilot", "CoPilot", "Flight Attendant"):
            self._show_crew_options()
        elif self.current_user_role == "Customer Support":
            self._show_customer_support_options()
        elif self.current_user_role == "Passenger":
            self._show_passenger_options()
        else:
            messagebox.showerror("Error", "Unknown user role.")

        ttk.Button(self, text="Logout", command=self._logout).pack(pady=10, anchor="s")

    def _show_admin_options(self):
        ttk.Label(self, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Manage Airlines", command=self._manage_airlines).pack(pady=5)
        ttk.Button(self, text="Manage Aircrafts", command=self._manage_aircrafts).pack(pady=5)
        ttk.Button(self, text="Manage Crews", command=self._manage_crews).pack(pady=5)
        ttk.Button(self, text="Manage Flights", command=self._load_flight_app).pack(pady=5)
        ttk.Button(self, text="View Reports", command=self._view_reports).pack(pady=5)

    def _manage_airlines(self):
        airline_app = AirlineApp(self)
        airline_app._show_manage_airline_options()
        airline_app.pack(fill="both", expand=True)
        self.title(f"Manage Airlines - {self.current_user_role.capitalize()}")

    def _manage_aircrafts(self):
        aircraft_app = AircraftApp(self)
        aircraft_app._show_manage_aircraft_options()
        aircraft_app.pack(fill="both", expand=True)
        self.title(f"Manage Aircrafts - {self.current_user_role.capitalize()}")

    def _load_flight_app(self):
        flight_app = FlightApp(self)
        flight_app._show_manage_flight_options()
        flight_app.pack(fill="both", expand=True)
        self.title(f"Skyline Airways System - Flights ({self.current_user_role.capitalize()})")


    def _manage_crews(self):
        crew_app = CrewApp(self)
        crew_app._show_manage_crew_options()
        crew_app.pack(fill="both", expand=True)
        self.title(f"Manage Crews - {self.current_user_role.capitalize()}")

    def _view_reports(self):
        report_app = ReportApp(self)
        report_app._show_manage_report_options()
        report_app.pack(fill="both", expand=True)
        self.title(f"Manage Report_app - {self.current_user_role.capitalize()}")


#Crew Options Here
    def _show_crew_options(self):
        ttk.Label(self, text="Crew Member Dashboard", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="View Flight Schedule", command=self._load_crew_schedule_view).pack(pady=5)  # Direct call
        # ttk.Button(self, text="Update Flight Status", command=self._open_update_flight_status_window).pack(pady=5)

        if not self.crew_app_instance:
            self.crew_app_instance = CrewApp(self, self.current_user_id)  # Create and pass ID

    def _load_crew_schedule_view(self):
        if self.crew_app_instance:
            self.crew_app_instance._view_crew_flight_schedule()
            self.crew_app_instance.pack(fill="both", expand=True)
            self.title(f"Your Flight Schedule - {self.current_user_role.capitalize()}")
        else:
            messagebox.showinfo("Info", "Crew dashboard not initialized.")

    def _show_customer_support_options(self):
        ttk.Label(self, text="Customer Support Portal", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="View Open Issues", command=lambda: messagebox.showinfo("Support Action", "View Open Issues")).pack(pady=5)
        ttk.Button(self, text="Resolve Issues", command=lambda: messagebox.showinfo("Support Action", "Resolve Issues")).pack(pady=5)

    def _show_passenger_options(self):
        ttk.Label(self, text="Passenger Portal", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="Book Flight", command=lambda: messagebox.showinfo("Passenger Action", "Book Flight")).pack(pady=5)
        ttk.Button(self, text="View/Cancel Bookings", command=self._view_passenger_bookings).pack(pady=5)

    def _view_passenger_bookings(self):
        if self.current_user_role == "Passenger":
            db = next(get_db())
            bookings = self.booking_service.get_passenger_bookings(db, self.current_user_id)
            db.close()
            if bookings:
                bookings_text = "Your Bookings:\n"
                for booking in bookings:
                    bookings_text += f"Flight: {booking['flight_number']}, From: {booking['departure_from']}, To: {booking['destination']}, Depart: {booking['departure_time']}, Seat: {booking['seat_no']}, Status: {booking['status']}\n"
                messagebox.showinfo("Your Bookings", bookings_text)
            else:
                messagebox.showinfo("Your Bookings", "No bookings found for your account.")
        else:
            messagebox.showerror("Error", "This action is only for passengers.")

    def _logout(self):
        self.current_user_id = None
        self.current_user_role = None
        for widget in self.winfo_children():
            widget.destroy()
        self.title("Skyline Airways System - Login")
        self.geometry("500x500")
        self._create_login_widgets()

if __name__ == "__main__":
    app = RootApp()
    app.mainloop()