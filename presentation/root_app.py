import tkinter as tk
from tkinter import ttk, messagebox
from business_logic.authentication_service import AuthenticationService
from business_logic.flight_service import FlightService
from business_logic.booking_service import BookingService
# from data_access.db_connect import get_db
# from database.initialize_db import init_db
from database.db_connection import get_db, init_db

class RootApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Skyline Airways System - Login")
        self.geometry("300x200")
        init_db()
        self.resizable(False, False)
        self.auth_service = AuthenticationService()
        self.flight_service = FlightService()
        self.booking_service = BookingService()
        self.current_user_id = None
        self.current_user_role = None

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
        ttk.Button(self, text="Manage Airlines", command=lambda: messagebox.showinfo("Admin Action", "Manage Airlines")).pack(pady=5)
        ttk.Button(self, text="Manage Aircrafts", command=lambda: messagebox.showinfo("Admin Action", "Manage Aircrafts")).pack(pady=5)
        ttk.Button(self, text="Manage Crews", command=lambda: messagebox.showinfo("Admin Action", "Manage Crews")).pack(pady=5)
        ttk.Button(self, text="Manage Flights", command=self._show_manage_flights).pack(pady=5)
        ttk.Button(self, text="View Reports", command=lambda: messagebox.showinfo("Admin Action", "View Reports")).pack(pady=5)

    def _show_manage_flights(self):
        # Example of how to use FlightService to get data
        db = next(get_db())
        all_flights = self.flight_service.list_all_flights(db)
        messagebox.showinfo("Manage Flights", f"Number of flights: {len(all_flights)}")
        db.close()
        # In a real application, you would display this data in a more user-friendly way
        # (e.g., in a Treeview widget) and provide options to create, update, and delete flights.

    def _show_crew_options(self):
        ttk.Label(self, text="Crew Member Dashboard", font=("Arial", 16)).pack(pady=20)
        ttk.Button(self, text="View Flight Schedule", command=self._view_flight_schedule).pack(pady=5)
        ttk.Button(self, text="Update Flight Status", command=lambda: messagebox.showinfo("Crew Action", "Update Flight Status")).pack(pady=5)

    def _view_flight_schedule(self):
        if self.current_user_role in ("Pilot", "CoPilot", "Flight Attendant"):
            db = next(get_db())
            schedule = self.flight_service.get_flight_schedule_for_crew(db, self.current_user_id)
            db.close()
            if schedule:
                schedule_text = "Your Flight Schedule:\n"
                for flight in schedule:
                    schedule_text += f"Flight: {flight['number']}, From: {flight['departure_from']}, To: {flight['destination']}, Depart: {flight['departure_time']}, Arrive: {flight['arrival_time']}\n"
                messagebox.showinfo("Flight Schedule", schedule_text)
            else:
                messagebox.showinfo("Flight Schedule", "No flights scheduled for you.")
        else:
            messagebox.showerror("Error", "This action is only for crew members.")

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
        self.geometry("300x200")
        self._create_login_widgets()

if __name__ == "__main__":
    app = RootApp()
    app.mainloop()