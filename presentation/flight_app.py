import tkinter as tk
import webbrowser
import pandas as pd
import plotly.express as px
from tkinter import ttk, messagebox
from database.db_connection import get_db, init_db
from business_logic.flight_service import FlightService
from business_logic.aircraft_service import AircraftService

class FlightApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self._create_widgets()
        self.flight_service = FlightService()


    def _create_widgets(self):
        ttk.Label(self, text="Flights", font=("Arial", 16)).pack(pady=10)

        # window option here
    def _show_manage_flight_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Manage Flights")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Manage Flight Options").pack(pady=10)

        ttk.Button(mfw, text="Manage All Flights", command=self._get_all_flights).pack(pady=10)
        ttk.Button(mfw, text="Get Flights by Status", command=self._get_flights_by_status_input).pack(pady=10)
        ttk.Button(mfw, text="Visualize Flights by Status", command=self._visualize_flights_by_status).pack(pady=10)
        # ttk.Button(mfw, text="Get Flight by id", command=self._get_flight_by_id_input).pack(pady=10)

    def _get_all_flights(self):
        afw = tk.Toplevel(self)
        afw.title("All Flights")

        self.flights_tree = ttk.Treeview(afw, columns=(
            "ID", "Number", "Status", "Ticket Cost", "Departure From", "Destination", "Departure Time", "Arrival Time",
            'Created At', "Updated At"
        ), show="headings")
        self.flights_tree.heading("#1", text="ID")
        self.flights_tree.heading("#2", text="Number")
        self.flights_tree.heading("#3", text="Status")
        self.flights_tree.heading("#4", text="Ticket Cost")
        self.flights_tree.heading("#5", text="Departure From")
        self.flights_tree.heading("#6", text="Destination")
        self.flights_tree.heading("#7", text="Departure Time")
        self.flights_tree.heading("#8", text="Arrival Time")
        self.flights_tree.heading("#9", text="Created At")
        self.flights_tree.heading("#10", text="Updated At")
        self._populate_flights_tree(self.flights_tree)

        self.flights_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for actions
        button_frame = ttk.Frame(afw)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Update Flight", command=self._open_update_flight_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Flight", command=self._delete_selected_flight).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Add New Flight", command=self._open_add_flight_form).pack(side="left", padx=5)

    def _populate_flights_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        db = next(get_db())
        try:
            all_flights = self.flight_service.list_all_flights(db)
            if all_flights:
                for flight in all_flights:
                    tree.insert('', "end", values=(
                        flight.id, flight.number, flight.status, flight.ticket_cost,
                        flight.departure_from, flight.destination, flight.departure_time,
                        flight.arrival_time, flight.created_at, flight.updated_at
                    ))
            else:
                messagebox.showinfo("All Flights", "No flights found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flights: {e}")
        finally:
            db.close()

    def _get_flights_by_status_input(self):
        status_window = tk.Toplevel(self)
        status_window.title("Get Flights by Status")
        ttk.Label(status_window, text="Select Status:").pack(pady=10)
        status_options = ['Scheduled', 'Cancelled', 'Delayed', 'Completed']
        self.status_var = tk.StringVar(status_window)
        self.status_var.set(status_options[0])
        status_dropdown = ttk.Combobox(status_window, textvariable=self.status_var, values=status_options, state="readonly")
        status_dropdown.pack(pady=5)

        get_flights_button = ttk.Button(status_window, text="Get Flights", command=self._fetch_flights)
        get_flights_button.pack(pady=15)

    def _fetch_flights(self):
        status = self.status_var.get()
        db = next(get_db())
        try:
            flights = self.flight_service.get_flights_by_status(db, status)
            if flights:
                self._display_flights(flights, status)
            else:
                messagebox.showerror("Error", "No flights found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flights: {e}")
        finally:
            db.close()


    def _display_flights(self, flights, status):
        display_window = tk.Toplevel(self)
        display_window.title(f"Flights with Status: {status}")
        print('I am here')
        if not flights:
            ttk.Label(display_window, text=f"No flights found with status: {status}").pack(padx=10, pady=10)
            return

        tree = ttk.Treeview(display_window, columns=("Number", "Departure", "Destination", "Time"))
        tree.heading("#1", text="Flight Number")
        tree.heading("#2", text="Departure From")
        tree.heading("#3", text="Destination")
        tree.heading("#4", text="Departure Time")
        tree.pack(expand=True, fill="both", padx=10, pady=10)

        for flight in flights:
            tree.insert('', "end", values=(
                flight.number,
                flight.departure_from,
                flight.destination,
                flight.departure_time
            ))


    def _get_flight_by_id_input(self):
        id_window = tk.Toplevel(self)
        id_window.title("Get Flight by ID")
        ttk.Label(id_window, text="Enter Flight ID:").pack(pady=5)
        id_entry = ttk.Entry(id_window)
        id_entry.pack(pady=5)
        ttk.Button(id_window, text="Get Flight", command=self._fetch_flight_by_id(id_entry.get()))

    def _fetch_flight_by_id(self, flight_id, window):
        db = next(get_db())
        try:
            flight = self.flight_service.get_flight_by_id(db, flight_id)
            if flight:
                messagebox.showinfo("Flight Details", f"Number: {flight.number}, Status: {flight.status}")
            else:
                messagebox.showinfo("Flight Details", f"Flight with ID '{flight_id}' not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flight: {e}")
        finally:
            db.close()
        window.destroy()

    def _open_add_flight_form(self):
        self.add_flight_window = tk.Toplevel(self)
        self.add_flight_window.title("Add New Flight")

        # Fetch available aircraft IDs for the dropdown
        db = next(get_db())
        aircraft_service = AircraftService()
        aircrafts = aircraft_service.list_all_aircrafts(db)
        aircraft_ids = [aircraft.id for aircraft in aircrafts]
        db.close()

        ttk.Label(self.add_flight_window, text="Flight Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_number_entry = ttk.Entry(self.add_flight_window)
        self.add_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_flight_window, text="Aircraft ID:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_aircraft_combo = ttk.Combobox(self.add_flight_window, values=aircraft_ids, state="readonly")
        self.add_aircraft_combo.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_flight_window, text="Ticket Cost:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.add_ticket_cost_entry = ttk.Entry(self.add_flight_window)
        self.add_ticket_cost_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_flight_window, text="Departure From:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.add_departure_from_entry = ttk.Entry(self.add_flight_window)
        self.add_departure_from_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_flight_window, text="Destination:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.add_destination_entry = ttk.Entry(self.add_flight_window)
        self.add_destination_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_flight_window, text="Departure Time (YYYY-MM-DD HH:MM:SS):").grid(row=5, column=0, padx=5,
                                                                                             pady=5, sticky="w")
        self.add_departure_time_entry = ttk.Entry(self.add_flight_window)
        self.add_departure_time_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_flight_window, text="Arrival Time (YYYY-MM-DD HH:MM:SS):").grid(row=6, column=0, padx=5,
                                                                                           pady=5, sticky="w")
        self.add_arrival_time_entry = ttk.Entry(self.add_flight_window)
        self.add_arrival_time_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        save_button = ttk.Button(self.add_flight_window, text="Save", command=self._save_new_flight)
        save_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.add_flight_window.grid_columnconfigure(1, weight=1)

    def _save_new_flight(self):
        new_number = self.add_number_entry.get()
        new_aircraft_id = self.add_aircraft_combo.get()
        new_ticket_cost = self.add_ticket_cost_entry.get()
        new_departure_from = self.add_departure_from_entry.get()
        new_destination = self.add_destination_entry.get()
        new_departure_time = self.add_departure_time_entry.get()
        new_arrival_time = self.add_arrival_time_entry.get()

        if not new_number or not new_aircraft_id or not new_ticket_cost or not new_departure_from or not new_destination or not new_departure_time or not new_arrival_time:
            messagebox.showerror("Error", "Please fill in all flight details.")
            return

        try:
            aircraft_id_int = int(new_aircraft_id)
            ticket_cost_float = float(new_ticket_cost)
            # Basic format check for time (you might want more robust validation)
            # Example: YYYY-MM-DD HH:MM:SS
            if len(new_departure_time) != 19 or len(new_arrival_time) != 19:
                messagebox.showerror("Error", "Invalid date/time format. Please use YYYY-MM-DD HH:MM:SS")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid Aircraft ID or Ticket Cost.")
            return

        new_flight_data = {
            "number": new_number,
            "aircraft_id": aircraft_id_int,
            "ticket_cost": ticket_cost_float,
            "departure_from": new_departure_from,
            "destination": new_destination,
            "departure_time": new_departure_time,
            "arrival_time": new_arrival_time
        }
        db = next(get_db())
        flight_service = FlightService()
        try:
            success = flight_service.create_flight(db, new_flight_data)
            if success:
                messagebox.showinfo("Success", f"Flight '{new_number}' added successfully.")
                # Assuming you have a _populate_flights_tree method
                if hasattr(self, '_populate_flights_tree'):
                    self._populate_flights_tree(self.flights_tree)
                self.add_flight_window.destroy()
            else:
                messagebox.showerror("Error", f"Could not add flight '{new_number}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding new flight: {e}")
            db.rollback()
        finally:
            db.close()

    def _open_update_flight_form(self):
        selected_item = self.flights_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a flight to update.")
            return
        flight_id = self.flights_tree.item(selected_item[0])['values'][0]
        print(flight_id)
        db = next(get_db())
        try:
            flight = self.parent.flight_service.get_flight_by_id(db, flight_id)
            if flight:
                self.update_window = tk.Toplevel(self)
                self.update_window.title(f"Update Flight ID: {flight_id}")

                # Create labels and entry fields for each attribute
                ttk.Label(self.update_window, text="Flight Number:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                self.update_number_entry = ttk.Entry(self.update_window)
                self.update_number_entry.insert(0, flight.number)
                self.update_number_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Status:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                self.update_status_var = tk.StringVar(self.update_window)
                self.update_status_var.set(flight.status)
                status_options = ['Scheduled', 'Cancelled', 'Delayed', 'Completed']
                status_dropdown = ttk.Combobox(self.update_window, textvariable=self.update_status_var,
                                               values=status_options, state="readonly")
                status_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Ticket Cost:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                self.update_cost_entry = ttk.Entry(self.update_window)
                self.update_cost_entry.insert(0, str(flight.ticket_cost))
                self.update_cost_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Departure From:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
                self.update_departure_from_entry = ttk.Entry(self.update_window)
                self.update_departure_from_entry.insert(0, flight.departure_from)
                self.update_departure_from_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Destination:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
                self.update_destination_entry = ttk.Entry(self.update_window)
                self.update_destination_entry.insert(0, flight.destination)
                self.update_destination_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

                # ... Add similar entries for Departure Time and Arrival Time ...
                ttk.Label(self.update_window, text="Departure Time:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
                self.update_departure_time_entry = ttk.Entry(self.update_window)
                self.update_departure_time_entry.insert(0, str(flight.departure_time))  # Ensure proper formatting
                self.update_departure_time_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Arrival Time:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
                self.update_arrival_time_entry = ttk.Entry(self.update_window)
                self.update_arrival_time_entry.insert(0, str(flight.arrival_time))  # Ensure proper formatting
                self.update_arrival_time_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

                save_button = ttk.Button(self.update_window, text="Save Changes",
                                         command=lambda: self._update_flight(flight_id))
                save_button.grid(row=7, column=0, columnspan=2, pady=10)

                self.update_window.grid_columnconfigure(1, weight=1)  # Make entry fields expand

            else:
                messagebox.showerror("Error", f"Flight with ID {flight_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flight details: {e}")
        finally:
            db.close()

    def _update_flight(self, flight_id):
        updated_data = {
            "number": self.update_number_entry.get(),
            "status": self.update_status_var.get(),
            "ticket_cost": float(self.update_cost_entry.get()),
            "departure_from": self.update_departure_from_entry.get(),
            "destination": self.update_destination_entry.get(),
            "departure_time": self.update_departure_time_entry.get(),
            "arrival_time": self.update_arrival_time_entry.get(),
        }
        db = next(get_db())
        try:
            self.flight_service.update_flight(db, flight_id, updated_data)
            messagebox.showinfo("Success", f"Flight ID {flight_id} updated successfully.")
            self._populate_flights_tree(self.flights_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating flight: {e}")
        finally:
            db.close()


    def _delete_selected_flight(self):
        selected_item = self.flights_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a flight to delete.")
            return
        flight_id = self.flights_tree.item(selected_item[0])['values'][0]
        print(flight_id)
        db = next(get_db())
        try:
            self.flight_service.delete_flight(db, flight_id)
            print('I am her e4')
            messagebox.showinfo("Success", f"Flight ID {flight_id} deleted successfully.")
            self._populate_flights_tree(self.flights_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating flight: {e}")
        finally:
            db.close()

    def _visualize_flights_by_status(self):
        db = next(get_db())
        try:
            status_counts = self.flight_service.get_flight_status_counts(db)
            if status_counts:
                df = pd.DataFrame(status_counts)
                fig = px.bar(df, x='status', y='count',
                             title='Number of Flights by Status',
                             labels={'status': 'Flight Status', 'count': 'Number of Flights'})
                fig.show()
            else:
                messagebox.showinfo("Info", "No flight data available.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data: {e}")
        finally:
            db.close()

