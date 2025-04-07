# presentation/flight_app.py
import tkinter as tk
from tkinter import ttk
from presentation.app_config import AppConfig
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import plotly.graph_objects as go
from plotly.subplots import make_subplots


class FlightApp(ttk.Frame):  # Inherit from ttk.Frame for better tab integration
    def __init__(self, master: ttk.Notebook, config: AppConfig):
        super().__init__(master)
        self.config = config
        self.flight_service = config.get_flight_service()
        self.create_widgets()
        self.load_flights()

    # ... (rest of your FlightApp class code) ...


    def create_widgets(self):
        self.flight_list_frame = ttk.LabelFrame(self, text="Flights")
        self.flight_list_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.flight_tree = ttk.Treeview(self.flight_list_frame, columns=(
        "ID", "Number", "Status", "Cost", "Departure", "Destination", "Departure Time", "Arrival Time"), show="headings")
        for col in self.flight_tree["columns"]:
            self.flight_tree.heading(col, text=col)
            self.flight_tree.column(col, width=100)
        self.flight_tree.pack(fill="both", expand=True)

        self.controls_frame = ttk.Frame(self)
        self.controls_frame.pack(pady=5)

        ttk.Button(self.controls_frame, text="Refresh Flights", command=self.load_flights).pack(side="left", padx=5)
        ttk.Button(self.controls_frame, text="Show Status Chart (Matplotlib)",
                   command=self.show_status_chart_matplotlib).pack(side="left", padx=5)
        ttk.Button(self.controls_frame, text="Show Status Chart (Plotly)", command=self.show_status_chart_plotly).pack(
            side="left", padx=5)

    def load_flights(self):
        for item in self.flight_tree.get_children():
            self.flight_tree.delete(item)
        flights = self.flight_service.list_all_flights()
        if flights:
            for flight in flights:
                self.flight_tree.insert("", "end", values=(
                    flight.id, flight.number, flight.status, flight.ticket_cost,
                    flight.departure_from, flight.destination, flight.departure_time,
                    flight.arrival_time
                ))

    def show_status_chart_matplotlib(self):
        flights = self.flight_service.list_all_flights()
        status_counts = {}
        for flight in flights:
            status = flight['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        statuses = list(status_counts.keys())
        counts = list(status_counts.values())

        chart_window = tk.Toplevel(self.master)
        chart_window.title("Flight Status Distribution (Matplotlib)")
        fig, ax = plt.subplots()
        ax.bar(statuses, counts)
        ax.set_xlabel("Flight Status")
        ax.set_ylabel("Number of Flights")
        ax.set_title("Flight Status Distribution")

        canvas = FigureCanvasTkAgg(fig, master=chart_window)
        widget = canvas.get_tk_widget()
        widget.pack(fill="both", expand=True)
        canvas.draw()

    def show_status_chart_plotly(self):
        flights = self.flight_service.list_all_flights()
        status_counts = {}
        for flight in flights:
            status = flight['status']
            status_counts[status] = status_counts.get(status, 0) + 1

        labels = list(status_counts.keys())
        values = list(status_counts.values())

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, title='Flight Status Distribution')])
        fig.show()

#
# if __name__ == "__main__":
#     config = AppConfig()
#     root = tk.Tk()
#     root.title("Airline Reservation System")
#     notebook = ttk.Notebook(root)
#     notebook.pack(fill="both", expand=True)
#     flight_app = FlightApp(notebook, config)
#     notebook.add(flight_app, text="Flights")
#     root.mainloop()
