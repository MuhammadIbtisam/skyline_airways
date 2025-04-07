#
# import tkinter as tk
# from tkinter import ttk
# from presentation.app_config import AppConfig
# # from presentation.flight_list_window import FlightListWindow
# # from presentation.aircraft_list_window import AircraftListWindow
# # from presentation.airline_list_window import AirlineListWindow
# # from presentation.passenger_list_window import PassengerListWindow
# # Import other window modules as you create them
#
# class MainApp:
#     def __init__(self, config: AppConfig):
#         self.config = config
#         self.root = config.get_root()
#         self.notebook = ttk.Notebook(self.root)
#         self.notebook.pack(fill="both", expand=True)
#
#         # self.flight_list_tab = FlightListWindow(self.notebook, self.config)
#         # self.aircraft_list_tab = AircraftListWindow(self.notebook, self.config)
#         # self.airline_list_tab = AirlineListWindow(self.notebook, self.config)
#         # self.passenger_list_tab = PassengerListWindow(self.notebook, self.config)
#         # Create and add other tabs/windows here
#
#         self.notebook.add(self.flight_list_tab, text="Flights")
#         self.notebook.add(self.aircraft_list_tab, text="Aircraft")
#         self.notebook.add(self.airline_list_tab, text="Airlines")
#         self.notebook.add(self.passenger_list_tab, text="Passengers")
#         # Add other tabs to the notebook
#
#     def run(self):
#         self.config.run()
#
# if __name__ == "__main__":
#     config = AppConfig()
#     app = MainApp(config)
#     app.run()