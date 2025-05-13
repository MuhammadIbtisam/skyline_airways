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
from business_logic.airline_service import AirlineService
from business_logic.aircraft_service import AircraftService

class AirlineApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self._create_widgets()
        self.airline_service = AirlineService()
        self.aircraft_service = AircraftService()


    def _create_widgets(self):
        ttk.Label(self, text="Airlines", font=("Arial", 16)).pack(pady=10)

        # window option here
    def _show_manage_airline_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Manage Airlines")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Manage Airline Options").pack(pady=10)

        ttk.Button(mfw, text="Manage All Airlines", command=self._get_all_airlines).pack(pady=10)
        ttk.Button(mfw, text="Visualize Airlines", command=self._visualize_airlines_by_country).pack(pady=10)
        ttk.Button(mfw, text="Visualize Fleet Size (Plotly)", command=self._visualize_fleet_size_plotly).pack(pady=10)
        ttk.Button(mfw, text="Visualize Total Capacity (Matplotlib)", command=self._visualize_total_capacity_matplotlib).pack(pady=10)

    def _get_all_airlines(self):
        afw = tk.Toplevel(self)
        afw.title("All Airlines")

        self.airlines_tree = ttk.Treeview(afw, columns=(
            "ID", "Name", "Country"
        ), show="headings")
        self.airlines_tree.heading("#1", text="ID")
        self.airlines_tree.heading("#2", text="Name")
        self.airlines_tree.heading("#3", text="Country")
        self._populate_airlines_tree(self.airlines_tree)

        self.airlines_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for actions
        button_frame = ttk.Frame(afw)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Update Airline", command=self._open_update_airline_form).pack(side="left", padx=5)
        # ttk.Button(button_frame, text="Delete Airline", command=self._delete_selected_airline).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Add New Airline", command=self._open_add_airline_form).pack(side="left", padx=5)

    def _populate_airlines_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)
        db = next(get_db())
        try:
            all_airlines = self.airline_service.list_all_airlines(db)
            if all_airlines:
                for airline in all_airlines:
                    tree.insert('', "end", values=(
                        airline.id, airline.name, airline.country
                    ))
            else:
                messagebox.showinfo("All Airlines", "No airlines found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching airlines: {e}")
        finally:
            db.close()

    def _open_add_airline_form(self):
        self.add_airline_window = tk.Toplevel(self)
        self.add_airline_window.title("Add New Airline")

        ttk.Label(self.add_airline_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.add_name_entry = ttk.Entry(self.add_airline_window)
        self.add_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(self.add_airline_window, text="Country:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.add_country_entry = ttk.Entry(self.add_airline_window)
        self.add_country_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        save_button = ttk.Button(self.add_airline_window, text="Save", command=self._save_new_airline)
        save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.add_airline_window.grid_columnconfigure(1, weight=1)

    def _save_new_airline(self):
        new_name = self.add_name_entry.get()
        new_country = self.add_country_entry.get()

        if not new_name or not new_country:
            messagebox.showerror("Error", "Please enter both name and country.")
            return

        new_airline_data = {"name": new_name, "country": new_country}
        db = next(get_db())
        try:
            success = self.airline_service.create_airline(db, new_airline_data)
            if success:
                messagebox.showinfo("Success", f"Airline '{new_name}' added successfully.")
                self._populate_airlines_tree(self.airlines_tree)  # Refresh the treeview
                self.add_airline_window.destroy()
            else:
                messagebox.showerror("Error", f"Could not add airline '{new_name}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Error adding new airline: {e}")
            db.rollback()
        finally:
            db.close()

    def _open_update_airline_form(self):
        selected_item = self.airlines_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a airline to update.")
            return
        airline_id = self.airlines_tree.item(selected_item[0])['values'][0]
        print(airline_id)
        db = next(get_db())
        try:
            airline = self.airline_service.get_airline_by_id(db, airline_id)
            if airline:
                self.update_window = tk.Toplevel(self)
                self.update_window.title(f"Update Airline ID: {airline_id}")

                # Create labels and entry fields for each attribute
                ttk.Label(self.update_window, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
                self.update_name_entry = ttk.Entry(self.update_window)
                self.update_name_entry.insert(0, airline.name)
                self.update_name_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Country:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
                self.update_country_entry = tk.Entry(self.update_window)
                self.update_country_entry.insert(0, airline.country)
                self.update_country_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

                save_button = ttk.Button(self.update_window, text="Save Changes",
                                         command=lambda: self._update_airline(airline_id))
                save_button.grid(row=7, column=0, columnspan=2, pady=10)

                self.update_window.grid_columnconfigure(1, weight=1)  # Make entry fields expand

            else:
                messagebox.showerror("Error", f"Airline with ID {airline_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching airline details: {e}")
        finally:
            db.close()

    def _update_airline(self, airline_id):
        updated_data = {
            "name": self.update_name_entry.get(),
            "country": self.update_country_entry.get()
        }
        db = next(get_db())
        try:
            self.airline_service.update_airline(db, airline_id, updated_data)
            messagebox.showinfo("Success", f"Airline ID {airline_id} updated successfully.")
            self._populate_airlines_tree(self.airlines_tree)
            self.update_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating airline: {e}")
        finally:
            db.close()

    def _delete_selected_airline(self):
        selected_item = self.airlines_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an airline to delete.")
            return
        airline_id = self.airlines_tree.item(selected_item[0])['values'][0]
        print(f"Attempting to delete airline with ID: {airline_id}")
        db = next(get_db())
        try:
            # First, delete all aircraft associated with this airline
            aircrafts_to_delete = self.aircraft_service.get_aircrafts_by_airline(db, airline_id)
            for aircraft in aircrafts_to_delete:
                self.aircraft_service.delete_aircraft(db, aircraft.id)
            print(f"Deleted {len(aircrafts_to_delete)} associated aircraft.")

            # Now, delete the airline
            success = self.airline_service.delete_airline(db, airline_id)
            if success:
                print('Airline deleted successfully.')
                messagebox.showinfo("Success", f"Airline ID {airline_id} and associated aircraft deleted successfully.")
                self._populate_airlines_tree(self.airlines_tree)
                if hasattr(self, 'update_window') and self.update_window.winfo_exists():
                    self.update_window.destroy()
            else:
                messagebox.showerror("Error", f"Airline with ID {airline_id} not found or could not be deleted.")
            db.commit()  # Commit the changes after deleting aircraft and airline
        except Exception as e:
            db.rollback()
            messagebox.showerror("Error", f"Error deleting airline and associated aircraft: {e}")
        finally:
            db.close()

    def _visualize_airlines_by_country(self): # Renamed method
        db = next(get_db())
        try:
            all_airlines = self.airline_service.list_all_airlines(db)
            if all_airlines:
                df = pd.DataFrame([airline.__dict__ for airline in all_airlines])
                if 'country' in df.columns:
                    country_counts = df['country'].value_counts().reset_index()
                    country_counts.columns = ['country', 'count']

                    fig = px.bar(country_counts, x='country', y='count',
                                 title='Number of Airlines by Country',
                                 labels={'country': 'Country', 'count': 'Number of Airlines'})

                    # Save the Plotly chart to an HTML file
                    temp_file_path = os.path.abspath("airlines_by_country.html")
                    fig.write_html(temp_file_path)

                    # Open the HTML file in the default web browser
                    webbrowser.open("file://" + temp_file_path)
                else:
                    messagebox.showerror("Error", "No 'country' information available for visualization.")
            else:
                messagebox.showinfo("Info", "No airlines data available to visualize.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching airline data for visualization: {e}")
        finally:
            db.close()

    def _visualize_fleet_size_plotly(self):
        db = next(get_db())
        try:
            airline_aircraft_data = self.airline_service.get_airline_fleet_size(db)

            if airline_aircraft_data:
                df = pd.DataFrame(airline_aircraft_data)
                fig = px.bar(df, x='airline_name', y='num_aircraft',
                             title='Number of Aircraft per Airline',
                             labels={'airline_name': 'Airline', 'num_aircraft': 'Number of Aircraft'})
                fig.show()
            else:
                messagebox.showinfo("Info", "No airline or aircraft data available.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data for visualization: {e}")
        finally:
            db.close()

    def _visualize_total_capacity_matplotlib(self):
        db = next(get_db())
        try:
            airline_capacity_data = self.airline_service.get_total_fleet_capacity(db)
            if airline_capacity_data:
                df = pd.DataFrame(airline_capacity_data)
                plt.figure(figsize=(10, 6))
                plt.bar(df['airline_name'], df['total_capacity'])
                plt.xlabel('Airline')
                plt.ylabel('Total Capacity')
                plt.title('Total Fleet Capacity per Airline')
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                plt.show()
            else:
                messagebox.showinfo("Info", "No airline or aircraft data available.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching data for visualization: {e}")
        finally:
            db.close()