import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.append(project_root)

from database.db_connection import get_db

from business_logic.customer_support_service import CustomerSupportService


class CustomerSupportApp(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self._create_widgets()
        # self.crew_service = CrewService()
        # self.flight_service = FlightService()
        self.support_service = CustomerSupportService()

    def _create_widgets(self):
        ttk.Label(self, text="Crews", font=("Arial", 16)).pack(pady=10)

    def _view_crew_options(self):
        mfw = tk.Toplevel(self)
        mfw.title("Customer Support Dashboard")
        mfw.geometry("950x600")

        ttk.Label(mfw, text="Customer Support Options").pack(pady=10)

        ttk.Button(mfw, text="Customer Support Issues", command=self._view_customer_support_issues).pack(pady=10)

    def _view_customer_support_issues(self):
        afw = tk.Toplevel(self)
        afw.title("Customer Support Issues")
        afw.geometry("800x600")  # Adjust size as needed

        self.issues_tree = ttk.Treeview(afw, columns=(
            "ID", "Reservation ID", "Issue", "Resolution", "Status", "Created At", "Updated At"
        ), show="headings")
        self.issues_tree.heading("#1", text="ID")
        self.issues_tree.heading("#2", text="Reservation ID")
        self.issues_tree.heading("#3", text="Issue")
        self.issues_tree.heading("#4", text="Resolution")
        self.issues_tree.heading("#5", text="Status")
        self.issues_tree.heading("#6", text="Created At")
        self.issues_tree.heading("#7", text="Updated At")
        self._populate_support_issues_tree(self.issues_tree)

        self.issues_tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Buttons for actions
        button_frame = ttk.Frame(afw)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="View Details", command=self._open_view_issue_details).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Update Resolution", command=self._open_update_issue_resolution).pack(side="left", padx=5)
        #                                                                                                     padx=5)
        # ttk.Button(button_frame, text="Mark as Closed", command=self._mark_issue_as_closed).pack(side="left", padx=5)

    def _populate_support_issues_tree(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        db = next(get_db())
        try:
            issues, error_message = self.support_service.get_customer_support_issues(db)
            if error_message:
                messagebox.showerror("Error", f"Error fetching support issues: {error_message}")
            elif issues:
                for issue in issues:
                    tree.insert('', "end", values=(
                        issue.id, issue.reservation_id, issue.issue, issue.resolution,
                        "Closed" if issue.is_closed else "Open", issue.created_at, issue.updated_at
                    ))
            else:
                messagebox.showinfo("Support Issues", "No support issues found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching support issues: {e}")
        finally:
            db.close()

    def _open_view_issue_details(self):
        selected_item = self.issues_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an issue to view details.")
            return
        issue_id = self.issues_tree.item(selected_item[0])['values'][0]
        db = next(get_db())
        try:
            issue, error_message = self.support_service.get_support_issue_by_id(db, issue_id)
            if error_message:
                messagebox.showerror("Error", f"Error fetching issue details: {error_message}")
            elif issue:
                details_window = tk.Toplevel(self)
                details_window.title(f"Issue ID: {issue.id} Details")
                ttk.Label(details_window, text=f"Reservation ID: {issue.reservation_id}").pack(padx=10, pady=5,
                                                                                               anchor="w")
                ttk.Label(details_window, text=f"Issue: {issue.issue}").pack(padx=10, pady=5, anchor="w")
                ttk.Label(details_window, text=f"Resolution: {issue.resolution}").pack(padx=10, pady=5, anchor="w")
                ttk.Label(details_window, text=f"Status: {'Closed' if issue.is_closed else 'Open'}").pack(padx=10,
                                                                                                          pady=5,
                                                                                                          anchor="w")
                ttk.Label(details_window, text=f"Created At: {issue.created_at}").pack(padx=10, pady=5, anchor="w")
                ttk.Label(details_window, text=f"Updated At: {issue.updated_at}").pack(padx=10, pady=5, anchor="w")
            else:
                messagebox.showinfo("Issue Details", f"Issue with ID {issue_id} not found.")
        finally:
            db.close()

    def _open_update_issue_resolution(self):
        selected_item = self.issues_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select an Issue to update.")
            return
        cs_issue_id = self.issues_tree.item(selected_item[0])['values'][0]
        print(cs_issue_id)
        db = next(get_db())
        try:
            issue, error_message = self.support_service.get_support_issue_by_id(db, cs_issue_id)
            if error_message:
                messagebox.showerror("Error", f"Error fetching issue details: {error_message}")
                return
            if issue:
                self.update_window = tk.Toplevel(self)
                self.update_window.title(f"Update Issue ID: {cs_issue_id}")

                ttk.Label(self.update_window, text=f"Reservation ID: {issue.reservation_id}").grid(row=0, column=0,
                                                                                                   padx=5, pady=5,
                                                                                                   sticky="w")
                ttk.Label(self.update_window, text=f"Issue: {issue.issue}").grid(row=1, column=0, padx=5, pady=5,
                                                                                 sticky="w")

                ttk.Label(self.update_window, text="Resolution:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
                self.update_resolution_text = tk.Text(self.update_window, height=5, width=40)
                self.update_resolution_text.insert(tk.END, issue.resolution)
                self.update_resolution_text.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

                ttk.Label(self.update_window, text="Mark as Closed:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
                self.is_closed_var = tk.BooleanVar(self.update_window)
                self.is_closed_var.set(issue.is_closed)
                closed_checkbutton = ttk.Checkbutton(self.update_window, text="Closed", variable=self.is_closed_var)
                closed_checkbutton.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

                save_button = ttk.Button(self.update_window, text="Save Changes",
                                         command=lambda: self._update_issue(cs_issue_id))
                save_button.grid(row=4, column=0, columnspan=2, pady=10)

                self.update_window.grid_columnconfigure(1, weight=1)
            else:
                messagebox.showerror("Error", f"Customer Support Issue with ID {cs_issue_id} not found.")
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching Issue details: {e}")

        finally:
            db.close()

    def _update_issue(self, cs_issue_id):
        new_resolution = self.update_resolution_text.get("1.0", tk.END).strip()
        is_closed = self.is_closed_var.get()

        updated_data = {
            "resolution": new_resolution,
            "is_closed": is_closed
        }

        db = next(get_db())
        try:
            success, error_message = self.support_service.update_support_issue(db, cs_issue_id, updated_data)
            if success:
                messagebox.showinfo("Success", f"Issue ID {cs_issue_id} updated successfully.")
                self._populate_support_issues_tree(self.issues_tree)
                self.update_window.destroy()
            else:
                messagebox.showerror("Error", f"Error updating Issue: {error_message}")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating Issue: {e}")
        finally:
            db.close()