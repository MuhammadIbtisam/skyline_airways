import os
import sys
import tkinter as tk
import pandas as pd
import plotly.express as px
from tkinter import ttk, messagebox
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


from matplotlib import pyplot as plt

from database.db_connection import get_db, init_db
from business_logic.crew_service import CrewService
from business_logic.flight_service import FlightService


class CrewApp(ttk.Frame):
    def __init__(self, parent, current_user_id=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.root = parent
        self.current_user_id = current_user_id
        self._create_widgets()
        self.crew_service = CrewService()
        self.flight_service = FlightService()

    def _create_widgets(self):
        ttk.Label(self, text="Crews", font=("Arial", 16)).pack(pady=10)

    def _show_manage_crew_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Manage Crews")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Manage Crew Options").pack(pady=10)

        ttk.Button(mfw, text="Manage All Crews", command=self._get_all_crews).pack(pady=10)

    def _view_crew_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Crew Dashboard")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="View Crew Options").pack(pady=10)

        ttk.Button(mfw, text="View Crew Flight Schedule", command=self._view_crew_flight_schedule).pack(pady=10)


    def _get_all_crews(self):
        afw = tk.Toplevel(self)
        afw.title("All Crews")

        self.crews_tree = ttk.Treeview(afw, columns=(
            "ID", "First Name", "Last Name", "Email", "Phone", "Role"
        ), show="headings")
        self.crews_tree.heading("#1", text="ID")
        self.crews_tree.heading("#2", text="First Name")
        self.crews_tree.heading("#3", text="Last Name")
        self.crews_tree.heading("#4", text="Email")
        self.crews_tree.heading("#5", text="Phone")
        self.crews_tree.heading("#6", text="Role")
        self._populate_crews_tree(self.crews_tree)

        self.crews_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for actions
        button_frame = ttk.Frame(afw)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Update Crew", command=self._open_update_crew_form).pack(side="left",
                                                                                               padx=5)
        # ttk.Button(button_frame, text="Delete Crew", command=self._delete_selected_crew).pack(side="left",
        #                                                                                       padx=5)
        ttk.Button(button_frame, text="Add New Crew", command=self._open_add_crew_form).pack(side="left",
                                                                                             padx=5)

    def _populate_crews_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        db = next(get_db())
        try:
            all_crews = self.crew_service.list_all_crews(db)
            if all_crews:
                for crew in all_crews:
                    tree.insert('', "end", values=(
                        crew.id, crew.first_name, crew.last_name, crew.email, crew.phone, crew.role
                    ))
            else:
                messagebox.showinfo("All Crews", "No crews found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching crews: {e}")
        finally:
            db.close()

    def _open_update_crew_form(self):
        selected_item = self.crews_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a crew member to update.")
            return
        crew_id = self.crews_tree.item(selected_item[0])['values'][0]
        print(crew_id)
        db = next(get_db())
        try:
            crew = self.crew_service.get_crew_by_id(db, crew_id)
            if crew:
                self.update_window = tk.Toplevel(self)
                self.update_window.title(f"Update Crew ID: {crew_id}")

                ttk.Label(self.update_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                self.update_first_name_entry = ttk.Entry(self.update_window)
                self.update_first_name_entry.insert(0, crew.first_name)
                self.update_first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                self.update_last_name_entry = ttk.Entry(self.update_window)
                self.update_last_name_entry.insert(0, crew.last_name)
                self.update_last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                self.update_email_entry = ttk.Entry(self.update_window)
                self.update_email_entry.insert(0, crew.email)
                self.update_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
                self.update_phone_entry = ttk.Entry(self.update_window)
                self.update_phone_entry.insert(0, crew.phone)
                self.update_phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Role:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
                self.role_values = ['Admin', 'Pilot', 'CoPilot', 'Flight Attendant', 'Customer Support']
                self.update_role_combo = ttk.Combobox(self.update_window, values=self.role_values, state="readonly")
                self.update_role_combo.set(crew.role)
                self.update_role_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

                save_button = ttk.Button(self.update_window, text="Save Changes",
                                         command=lambda: self._update_crew(crew_id))
                save_button.grid(row=7, column=0, columnspan=2, pady=10)

                self.update_window.grid_columnconfigure(1, weight=1)  # Make entry fields expand

            else:
                messagebox.showerror("Error", f"Crew member with ID {crew_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching crew member details: {e}")
        finally:
            db.close()

    def _update_crew(self, crew_id):
        updated_data = {
            "first_name": self.update_first_name_entry.get(),
            "last_name": self.update_last_name_entry.get(),
            "email": self.update_email_entry.get(),
            "phone": self.update_phone_entry.get(),
            "role": self.update_role_combo.get()
        }
        db = next(get_db())
        try:
            self.crew_service.update_crew(db, crew_id, updated_data)
            messagebox.showinfo("Success", f"Crew member ID {crew_id} updated successfully.")
            self._populate_crews_tree(self.crews_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating crew member: {e}")
        finally:
            db.close()

    def _open_add_crew_form(self):
        self.add_crew_window = tk.Toplevel(self.root)
        self.add_crew_window.title("Add New Crew Member")

        ttk.Label(self.add_crew_window, text="First Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_first_name_entry = ttk.Entry(self.add_crew_window)
        self.add_first_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_crew_window, text="Last Name:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_last_name_entry = ttk.Entry(self.add_crew_window)
        self.add_last_name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_crew_window, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.add_email_entry = ttk.Entry(self.add_crew_window)
        self.add_email_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_crew_window, text="Phone:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.add_phone_entry = ttk.Entry(self.add_crew_window)
        self.add_phone_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_crew_window, text="Role:").grid(row=4, column=0, padx=5, pady=5, sticky="w")
        self.role_values = ['Admin', 'Pilot', 'CoPilot', 'Flight Attendant', 'Customer Support']
        self.add_role_combo = ttk.Combobox(self.add_crew_window, values=self.role_values, state="readonly")
        self.add_role_combo.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_crew_window, text="Username:").grid(row=5, column=0, padx=5, pady=5, sticky="w")
        self.add_username_entry = ttk.Entry(self.add_crew_window)
        self.add_username_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_crew_window, text="Password:").grid(row=6, column=0, padx=5, pady=5, sticky="w")
        self.add_password_entry = ttk.Entry(self.add_crew_window, show="*")
        self.add_password_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        save_button = ttk.Button(self.add_crew_window, text="Save", command=self._save_new_crew)
        save_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.add_crew_window.grid_columnconfigure(1, weight=1)

    def _save_new_crew(self):
        new_first_name = self.add_first_name_entry.get()
        new_last_name = self.add_last_name_entry.get()
        new_email = self.add_email_entry.get()
        new_phone = self.add_phone_entry.get()
        new_role = self.add_role_combo.get()
        new_username = self.add_username_entry.get()
        new_password = self.add_password_entry.get()

        if not all([new_first_name, new_last_name, new_phone, new_role, new_username, new_password]):
            messagebox.showerror("Error", "Please fill all required fields.")
            return
        db = next(get_db())
        try:
            crew_id = self.crew_service.create_crew(
                db,
                new_first_name,
                new_last_name,
                new_email,
                new_phone,
                new_role,
                new_username,
                new_password
            )
            if crew_id:
                messagebox.showinfo("Success",
                                    f"Crew member '{new_first_name} {new_last_name}' added successfully with User '{new_username}'.")
                self._populate_crews_tree(self.crews_tree)  # Refresh the treeview
                self.add_crew_window.destroy()
            else:
                messagebox.showerror("Error", f"Could not add crew member '{new_first_name} {new_last_name}' and user.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding new crew member and user: {e}")
            db.rollback()
        finally:
            db.close()

    def _delete_selected_crew(self):
        selected_item = self.crews_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a crew to delete.")
            return
        crew_id = self.crews_tree.item(selected_item[0])['values'][0]
        print(crew_id)
        db = next(get_db())
        try:
            self.crew_service.delete_crew(db, crew_id)
            messagebox.showinfo("Success", f"Crew ID {crew_id} deleted successfully.")
            self._populate_crews_tree(self.crews_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting crew: {e}")
        finally:
            db.close()

    def _visualize_crew_plotly(self):
        db = next(get_db())
        try:
            all_crews = self.crew_service.list_all_crews(db)
            if all_crews:
                df = pd.DataFrame([crew.__dict__ for crew in all_crews])
                if not df.empty:  # Check if the DataFrame is not empty
                    # 1. Distribution of Crew Capacity (Histogram)
                    fig_capacity = px.histogram(df, x='capacity',
                                                title='Distribution of Crew Capacity',
                                                labels={'capacity': 'Crew Capacity', 'count': 'Number of Crew'},
                                                marginal="rug")
                    fig_capacity.show()

                    # 2. Crew Count by Model (Bar Chart)
                    model_counts = df['model'].value_counts().reset_index()
                    model_counts.columns = ['model', 'count']
                    fig_models = px.bar(model_counts, x='model', y='count',
                                        title='Number of Crew by Model',
                                        labels={'model': 'Crew Model', 'count': 'Number of Crew'})
                    fig_models.show()
                else:
                    messagebox.showinfo("Info", "No crew data available for visualization.")
            else:
                messagebox.showinfo("Info", "No crew data available to visualize.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching crew data for visualization: {e}")
        finally:
            db.close()

    def _visualize_crew_matplotlib_tk(self):
        db = next(get_db())
        try:
            all_crews = self.crew_service.list_all_crews(db)
            if all_crews:
                df = pd.DataFrame([crew.__dict__ for crew in all_crews])
                if not df.empty:
                    # 1. Distribution of Crew Capacity (Histogram)
                    plt.figure(figsize=(8, 6))
                    plt.hist(df['capacity'], bins=10, edgecolor='black')
                    plt.xlabel('Crew Capacity')
                    plt.ylabel('Number of Crew')
                    plt.title('Distribution of Crew Capacity')
                    plt.grid(True)
                    plt.show()

                    # 2. Crew Count by Model (Bar Chart)
                    model_counts = df['model'].value_counts()
                    plt.figure(figsize=(10, 6))
                    plt.bar(model_counts.index, model_counts.values)
                    plt.xlabel('Crew Model')
                    plt.ylabel('Number of Crew')
                    plt.title('Number of Crew by Model')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.show()
                else:
                    messagebox.showinfo("Info", "No crew data available for visualization.")
            else:
                messagebox.showinfo("Info", "No crew data available to visualize.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching crew data for visualization: {e}")
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
                save_button = ttk.Button(self.update_window, text="Save Changes",
                                         command=lambda: self._update_flight(flight_id))
                save_button.grid(row=7, column=0, columnspan=2, pady=10)

                self.update_window.grid_columnconfigure(1, weight=1)
            else:
                messagebox.showerror("Error", f"Flight with ID {flight_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flight details: {e}")

        finally:
            db.close()

    def _update_flight(self, flight_id):
        updated_data = {
            "status": self.update_status_var.get()
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

    def _view_crew_flight_schedule(self):
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

    def _populate_flights_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        if self.current_user_id is None:
            messagebox.showerror("Error", "Current user ID not available.")
            return

        db = next(get_db())
        try:
            flights, error_message = self.crew_service.get_crew_flight_schedule(db, self.current_user_id)
            if error_message:
                messagebox.showerror("Error", f"Error fetching flights: {error_message}")
            elif flights is not None:
                for flight in flights:
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