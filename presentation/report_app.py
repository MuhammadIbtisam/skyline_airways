
import tkinter as tk
import pandas as pd
import plotly.express as px
from tkinter import ttk, messagebox

from matplotlib import pyplot as plt

from database.db_connection import get_db, init_db
from business_logic.report_service import ReportService

class ReportApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self._create_widgets()
        self.report_service = ReportService()


    def _create_widgets(self):
        ttk.Label(self, text="Reports", font=("Arial", 16)).pack(pady=10)

        # window option here
    def _show_manage_report_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Manage Reports")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Manage Reports Options").pack(pady=10)

        ttk.Button(mfw, text="Visualize Flight Status Overview", command=self._visualize_flight_status_overview_plotly).pack(pady=10)
        ttk.Button(mfw, text="Visualize Revenue per Airline", command=self._visualize_revenue_per_airline_plotly).pack(pady=10)
        ttk.Button(mfw, text="Visualize Passenger Traffic by Route", command=self._visualize_passenger_traffic_by_route_plotly).pack(pady=10)
        ttk.Button(mfw, text="Visualize Support Issues by Category", command=self._visualize_customer_support_issues_plotly).pack(pady=10)
        # ttk.Button(mfw, text="Visualize Aircrafts Matplotlib", command=self._visualize_aircraft_matplotlib_tk).pack(pady=10)


    def _visualize_flight_status_overview_plotly(self):
        db = next(get_db())
        try:
            status_overview_data = self.report_service.get_flight_status_overview(db)

            if status_overview_data:
                df = pd.DataFrame(status_overview_data)
                fig = px.pie(df, names='status', values='count',
                             title='Flight Status Overview',
                             labels={'status': 'Flight Status', 'count': 'Number of Flights'},
                             hole=0.3)  # Adding a hole makes it a donut chart for better visual appeal
                fig.update_traces(textinfo='percent+label',
                                  pull=[0.05] * len(df))  # Add percentage and label, slightly pull slices
                fig.show()
            else:
                messagebox.showinfo("Info", "No flight data available for status overview.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching flight status overview data: {e}")
        finally:
            db.close()

    def _visualize_revenue_per_airline_plotly(self):
        db = next(get_db())
        try:
            revenue_data = self.report_service.get_total_revenue_per_airline(db)

            if revenue_data:
                df = pd.DataFrame(revenue_data)
                fig = px.bar(df, x='airline_name', y='total_revenue',
                             title='Total Revenue per Airline',
                             labels={'airline_name': 'Airline', 'total_revenue': 'Total Revenue (GBP)'})
                fig.show()
            else:
                messagebox.showinfo("Info", "No revenue data available.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching revenue data: {e}")
        finally:
            db.close()

    def _visualize_passenger_traffic_by_route_plotly(self):
        db = next(get_db())
        try:
            traffic_data = self.report_service.get_passenger_traffic_by_route(db)

            if traffic_data:
                df = pd.DataFrame(traffic_data)
                df['route'] = df['departure_from'] + ' - ' + df['destination']
                fig = px.bar(df, x='route', y='passenger_count',
                             title='Passenger Traffic by Flight Route',
                             labels={'route': 'Flight Route', 'passenger_count': 'Number of Passengers'})
                fig.show()
            else:
                messagebox.showinfo("Info", "No passenger traffic data available.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching passenger traffic data: {e}")
        finally:
            db.close()

    def _visualize_customer_support_issues_plotly(self):
        db = next(get_db())
        try:
            issues_data = self.report_service.get_customer_support_issues_by_category(db)

            if issues_data:
                df = pd.DataFrame(issues_data)
                fig = px.bar(df, x='issue', y='count',
                             title='Customer Support Issues by Category',
                             labels={'issue': 'Issue Category', 'count': 'Number of Issues'})
                fig.show()
            else:
                messagebox.showinfo("Info", "No customer support issue data available.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching customer support issue data: {e}")
        finally:
            db.close()