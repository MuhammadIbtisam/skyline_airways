import os
import sys
import tkinter as tk
import webbrowser
import pandas as pd
import plotly.express as px
from tkinter import ttk, messagebox

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)


from matplotlib import pyplot as plt

from database.db_connection import get_db, init_db
from business_logic.aircraft_service import AircraftService

class AircraftApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self._create_widgets()
        self.aircraft_service = AircraftService()


    def _create_widgets(self):
        ttk.Label(self, text="Aircrafts", font=("Arial", 16)).pack(pady=10)

        # window option here
    def _show_manage_aircraft_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Manage Aircrafts")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Manage Aircraft Options").pack(pady=10)

        ttk.Button(mfw, text="Manage All Aircrafts", command=self._get_all_aircrafts).pack(pady=10)
        ttk.Button(mfw, text="Visualize Aircrafts Plotly", command=self._visualize_aircraft_plotly).pack(pady=10)
        ttk.Button(mfw, text="Visualize Aircrafts Matplotlib", command=self._visualize_aircraft_matplotlib_tk).pack(pady=10)

    def _get_all_aircrafts(self):
        afw = tk.Toplevel(self)
        afw.title("All Aircrafts")

        self.aircrafts_tree = ttk.Treeview(afw, columns=(
            "ID", "Airline ID", "Model", "Capacity", "Created At"
        ), show="headings")
        self.aircrafts_tree.heading("#1", text="ID")
        self.aircrafts_tree.heading("#2", text="Airline ID")
        self.aircrafts_tree.heading("#3", text="Model")
        self.aircrafts_tree.heading("#4", text="Capacity")
        self.aircrafts_tree.heading("#5", text="Created At")
        self._populate_aircrafts_tree(self.aircrafts_tree)

        self.aircrafts_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for actions
        button_frame = ttk.Frame(afw)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Update Aircraft", command=self._open_update_aircraft_form).pack(side="left",
                                                                                                       padx=5)
        # ttk.Button(button_frame, text="Delete Aircraft", command=self._delete_selected_aircraft).pack(side="left",
        #                                                                                               padx=5)
        ttk.Button(button_frame, text="Add New Aircraft", command=self._open_add_aircraft_form).pack(side="left",
                                                                                                     padx=5)

    def _populate_aircrafts_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        db = next(get_db())
        try:
            all_aircrafts = self.aircraft_service.list_all_aircrafts(db)
            if all_aircrafts:
                for aircraft in all_aircrafts:
                    tree.insert('', "end", values=(
                        aircraft.id, aircraft.airline_id, aircraft.model, aircraft.capacity, aircraft.created_at
                    ))
            else:
                messagebox.showinfo("All Aircrafts", "No aircrafts found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching aircrafts: {e}")
        finally:
            db.close()

    def _open_add_aircraft_form(self):
        add_aircraft_window = tk.Toplevel(self)
        add_aircraft_window.title("Add New Aircraft")
        # Add your form elements (Labels, Entry widgets, etc.) here
        # and a Save button that calls a _save_new_aircraft method

    def _open_update_aircraft_form(self):
        selected_item = self.aircrafts_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an aircraft to update.")
            return
        aircraft_id = self.aircrafts_tree.item(selected_item[0])['values'][0]
        print(aircraft_id)
        db = next(get_db())
        try:
            aircraft = self.aircraft_service.get_aircraft_by_id(db, aircraft_id)
            if aircraft:
                self.update_window = tk.Toplevel(self)
                self.update_window.title(f"Update Aircraft ID: {aircraft_id}")

                ttk.Label(self.update_window, text="Airline ID:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                self.update_airline_id_entry = ttk.Entry(self.update_window)
                self.update_airline_id_entry.insert(0, aircraft.airline_id)
                self.update_airline_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Model:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                self.update_model_entry = ttk.Entry(self.update_window)
                self.update_model_entry.insert(0, aircraft.model)
                self.update_model_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Capacity:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                self.update_capacity_entry = ttk.Entry(self.update_window)
                self.update_capacity_entry.insert(0, aircraft.capacity)
                self.update_capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

                save_button = ttk.Button(self.update_window, text="Save Changes",
                                         command=lambda: self._update_aircraft(aircraft_id))
                save_button.grid(row=7, column=0, columnspan=2, pady=10)

                self.update_window.grid_columnconfigure(1, weight=1)  # Make entry fields expand

            else:
                messagebox.showerror("Error", f"Aircraft with ID {aircraft_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching aircraft details: {e}")
        finally:
            db.close()

    def _update_aircraft(self, aircraft_id):
        updated_data = {
            "airline_id": self.update_airline_id_entry.get(),
            "model": self.update_model_entry.get(),
            "capacity": self.update_capacity_entry.get()
        }
        db = next(get_db())
        try:
            self.aircraft_service.update_aircraft(db, aircraft_id, updated_data)
            messagebox.showinfo("Success", f"Aircraft ID {aircraft_id} updated successfully.")
            self._populate_aircrafts_tree(self.aircrafts_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating aircraft: {e}")
        finally:
            db.close()

    def _delete_selected_aircraft(self):
        selected_item = self.aircrafts_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a aircraft to delete.")
            return
        aircraft_id = self.aircrafts_tree.item(selected_item[0])['values'][0]
        print(aircraft_id)
        db = next(get_db())
        try:
            self.aircraft_service.delete_aircraft(db, aircraft_id)
            messagebox.showinfo("Success", f"Aircraft ID {aircraft_id} deleted successfully.")
            self._populate_aircrafts_tree(self.aircrafts_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting aircraft: {e}")
        finally:
            db.close()

    def _visualize_aircraft_plotly(self):
        db = next(get_db())
        try:
            all_aircrafts = self.aircraft_service.list_all_aircrafts(db)
            if all_aircrafts:
                df = pd.DataFrame([aircraft.__dict__ for aircraft in all_aircrafts])
                if not df.empty:  # Check if the DataFrame is not empty
                    # 1. Distribution of Aircraft Capacity (Histogram)
                    fig_capacity = px.histogram(df, x='capacity',
                                                title='Distribution of Aircraft Capacity',
                                                labels={'capacity': 'Aircraft Capacity', 'count': 'Number of Aircraft'},
                                                marginal="rug")
                    fig_capacity.show()

                    # 2. Aircraft Count by Model (Bar Chart)
                    model_counts = df['model'].value_counts().reset_index()
                    model_counts.columns = ['model', 'count']
                    fig_models = px.bar(model_counts, x='model', y='count',
                                        title='Number of Aircraft by Model',
                                        labels={'model': 'Aircraft Model', 'count': 'Number of Aircraft'})
                    fig_models.show()
                else:
                    messagebox.showinfo("Info", "No aircraft data available for visualization.")
            else:
                messagebox.showinfo("Info", "No aircraft data available to visualize.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching aircraft data for visualization: {e}")
        finally:
            db.close()

    def _visualize_aircraft_matplotlib_tk(self):
        db = next(get_db())
        try:
            all_aircrafts = self.aircraft_service.list_all_aircrafts(db)
            if all_aircrafts:
                df = pd.DataFrame([aircraft.__dict__ for aircraft in all_aircrafts])
                if not df.empty:
                    # 1. Distribution of Aircraft Capacity (Histogram)
                    plt.figure(figsize=(8, 6))
                    plt.hist(df['capacity'], bins=10, edgecolor='black')
                    plt.xlabel('Aircraft Capacity')
                    plt.ylabel('Number of Aircraft')
                    plt.title('Distribution of Aircraft Capacity')
                    plt.grid(True)
                    plt.show()

                    # 2. Aircraft Count by Model (Bar Chart)
                    model_counts = df['model'].value_counts()
                    plt.figure(figsize=(10, 6))
                    plt.bar(model_counts.index, model_counts.values)
                    plt.xlabel('Aircraft Model')
                    plt.ylabel('Number of Aircraft')
                    plt.title('Number of Aircraft by Model')
                    plt.xticks(rotation=45, ha='right')
                    plt.tight_layout()
                    plt.show()
                else:
                    messagebox.showinfo("Info", "No aircraft data available for visualization.")
            else:
                messagebox.showinfo("Info", "No aircraft data available to visualize.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching aircraft data for visualization: {e}")
        finally:
            db.close()