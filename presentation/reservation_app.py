import datetime
import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


from database.db_connection import get_db
from business_logic.reservation_service import ReservationService
from business_logic.flight_service import FlightService

class ReservationApp(ttk.Frame):
    def __init__(self, parent, current_user_id=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.current_user_id = current_user_id
        self._create_widgets()
        self.reservation_service = ReservationService()
        self.flight_service = FlightService()
        self._available_flight_numbers = []

        # self._populate_reservations() # Populate reservations when the window is created

    def _create_widgets(self):
        ttk.Label(self, text="Passenger Reservations", font=("Arial", 16)).pack(pady=10)
        # ttk.Button(self, text="Make New Reservation", command=self._open_new_reservation_form).pack(pady=5)

    def _load_passenger_bookings(self):
        mfw = tk.Toplevel(self)
        mfw.title("Passenger Reservations")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Passenger Options").pack(pady=10)

        ttk.Button(mfw, text="Passenger Reservations", command=self._passenger_reservations_view).pack(pady=10)

    def _passenger_reservations_view(self):
        afw = tk.Toplevel(self)
        afw.title("Passenger Reservations")
        afw.geometry("950x600")
        self.reservations_tree = ttk.Treeview(afw, columns=(
            "Flight Number", "Departure From", "Destination", "Departure Time", "Arrival Time", "Seat No", "Status", "Booking Date"
        ), show="headings")
        self.reservations_tree.heading("#1", text="Flight Number")
        self.reservations_tree.heading("#2", text="Departure From")
        self.reservations_tree.heading("#3", text="Destination")
        self.reservations_tree.heading("#4", text="Departure Time")
        self.reservations_tree.heading("#5", text="Arrival Time")
        self.reservations_tree.heading("#6", text="Seat no")
        self.reservations_tree.heading("#7", text="Status")
        self.reservations_tree.heading("#8", text="Booking Date")
        self._populate_reservations(self.reservations_tree)

        self.reservations_tree.pack(fill="both", expand=True, padx=10, pady=10)
        button_frame = ttk.Frame(afw)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Reservations", command=self._open_new_reservation_form).pack(side="left", padx=5)


    def _populate_reservations(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        db = next(get_db())
        try:
            reservations, error_message = self.reservation_service.get_passenger_reservations(db, self.current_user_id)
            if error_message:
                messagebox.showerror("Error", f"Error fetching reservations: {error_message}")
            elif reservations:
                for reservation in reservations:
                    tree.insert('', "end", values=(
                        reservation['flight_number'],
                        reservation['departure_from'],
                        reservation['destination'],
                        reservation['departure_time'],
                        reservation['arrival_time'],
                        reservation['seat_no'],
                        reservation['status'],
                        reservation['booking_date']
                    ))
            else:
                messagebox.showinfo("Reservations", "No reservations found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching reservations: {e}")
        finally:
            db.close()

    def _open_new_reservation_form(self):
        self.new_reservation_window = tk.Toplevel(self)
        self.new_reservation_window.title("Make New Reservation")

        # ttk.Label(self.new_reservation_window, text="Flight Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        # self.flight_number_var = tk.StringVar(self.new_reservation_window)
        # self.flight_number_var.set(self._available_flight_numbers[0] if self._available_flight_numbers else "")
        # self.flight_number_combo = ttk.Combobox(self.new_reservation_window, textvariable=self.flight_number_var,
        #                                         values=self._available_flight_numbers, state="readonly")
        # self.flight_number_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        db = next(get_db())
        flight_service = FlightService()
        flights = flight_service.list_all_flights(db)
        flight_ids = [flight.id for flight in flights]
        db.close()

        ttk.Label(self.new_reservation_window, text="Flight ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_flight_combo = ttk.Combobox(self.new_reservation_window, values=flight_ids, state="readonly")
        self.add_flight_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")



        ttk.Label(self.new_reservation_window, text="Seat Number:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.seat_number_entry = ttk.Entry(self.new_reservation_window)
        self.seat_number_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        save_button = ttk.Button(self.new_reservation_window, text="Reserve Seat", command=self._save_new_reservation)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.new_reservation_window.grid_columnconfigure(1, weight=1)

    def _save_new_reservation(self):
        flight_id = self.add_flight_combo.get()
        seat_number = self.seat_number_entry.get()

        if not flight_id or not seat_number:
            messagebox.showerror("Error", "Please select a Flight Number and enter a Seat Number.")
            return

        new_reservation_data = {
            'passenger_id': self.current_user_id,
            'flight_id': flight_id,
            'seat_no': seat_number,
            'booking_date': datetime.date.today()
        }
        db = next(get_db())
        try:
            success, error_message = self.reservation_service.reserve_seat(
                db, new_reservation_data
            )
            if success:
                messagebox.showinfo("Success", f"Seat '{seat_number}' reserved on Flight '{flight_id}'.")
                # self._view_passenger_reservations()  # Refresh the booking list
                self._populate_reservations(self.reservations_tree)
                self.new_reservation_window.destroy()
            else:
                messagebox.showerror("Error", f"Error reserving seat: {error_message}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            db.rollback()
        finally:
            db.close()

    def _populate_flight_numbers(self):
        db = next(get_db())
        try:
            flights, error_message = self.flight_service.list_all_flights(db)
            if error_message:
                messagebox.showerror("Error", f"Error fetching flight numbers: {error_message}")
            elif flights:
                available_flight_numbers = sorted([flight.number for flight in flights])
                return available_flight_numbers
            else:
                return []
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flight numbers: {e}")
            return []
        finally:
            db.close()

    # You likely don't need this method anymore as ReservationApp itself is the option view
    # def _view_passenger_options(self):
    #     pass

    # You should directly populate the reservations in the ReservationApp window
    # def _view_passenger_reservations(self):
    #     pass