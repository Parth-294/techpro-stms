import os
import sys
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3

# Ensure src directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import User, Customer, SupportEngineer, Admin
from database import DB_NAME, init_db, seed_demo_tickets

class TechProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TechPro Solutions - Service Ticket Management System")
        self.root.geometry("850x600")
        self.current_user = None
        
        # Ensure database exists and is seeded
        init_db()
        seed_demo_tickets()
        
        self.show_login_screen()

    def clear_window(self):
        """Destroy all widgets in the main window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login_screen(self):
        """Render the login window for role-based access control."""
        self.clear_window()
        
        # Header Frame
        header_frame = tk.Frame(self.root, bg="#1E3A8A", pady=20)
        header_frame.pack(fill=tk.X)
        tk.Label(header_frame, text="TechPro Solutions - STMS", font=("Arial", 18, "bold"), fg="white", bg="#1E3A8A").pack()
        tk.Label(header_frame, text="Service Ticket Management System", font=("Arial", 10), fg="#93C5FD", bg="#1E3A8A").pack()

        # Login Form Frame
        form_frame = tk.Frame(self.root, padx=20, pady=40)
        form_frame.pack(expand=True)

        tk.Label(form_frame, text="Username:", font=("Arial", 11)).grid(row=0, column=0, sticky=tk.W, pady=10)
        self.user_entry = tk.Entry(form_frame, font=("Arial", 11), width=25)
        self.user_entry.grid(row=0, column=1, pady=10, padx=10)

        tk.Label(form_frame, text="Password:", font=("Arial", 11)).grid(row=1, column=0, sticky=tk.W, pady=10)
        self.pass_entry = tk.Entry(form_frame, font=("Arial", 11), width=25, show="*")
        self.pass_entry.grid(row=1, column=1, pady=10, padx=10)

        login_btn = tk.Button(form_frame, text="Login", font=("Arial", 11, "bold"), bg="#2563EB", fg="white", width=15, command=self.handle_login)
        login_btn.grid(row=2, column=0, columnspan=2, pady=20)

        # Demo Credentials Hint
        hint_text = "Demo Accounts (Password: password123):\n• Admin: admin_boss\n• Engineer: eng_john\n• Customer: cust_alice"
        tk.Label(form_frame, text=hint_text, font=("Arial", 9, "italic"), fg="#6B7280", justify=tk.LEFT).grid(row=3, column=0, columnspan=2, pady=10)

    def handle_login(self):
        """Authenticate user and route to appropriate role dashboard."""
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        user = User.authenticate(username, password)
        if user:
            self.current_user = user
            messagebox.showinfo("Success", f"Welcome back, {user.username} ({user.role})!")
            self.load_dashboard()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def load_dashboard(self):
        """Route user to their specific dashboard based on role."""
        if self.current_user.role == "Customer":
            self.show_customer_dashboard()
        elif self.current_user.role == "SupportEngineer":
            self.show_engineer_dashboard()
        elif self.current_user.role == "Admin":
            self.show_admin_dashboard()

    def logout(self):
        """Log out current session and return to login screen."""
        self.current_user = None
        self.show_login_screen()

    # CUSTOMER DASHBOARD
    def show_customer_dashboard(self):
        self.clear_window()
        self.create_dashboard_header("Customer Dashboard")

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Submit Ticket Sub-Frame
        form_frame = tk.LabelFrame(main_frame, text="Submit New Support Ticket", font=("Arial", 11, "bold"), padx=15, pady=15)
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        tk.Label(form_frame, text="Title:", font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        title_entry = tk.Entry(form_frame, font=("Arial", 10), width=35)
        title_entry.pack(anchor=tk.W, pady=5)

        tk.Label(form_frame, text="Priority:", font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        priority_combo = ttk.Combobox(form_frame, values=["Low", "Medium", "High"], state="readonly", width=33)
        priority_combo.current(0)
        priority_combo.pack(anchor=tk.W, pady=5)

        tk.Label(form_frame, text="Description:", font=("Arial", 10)).pack(anchor=tk.W, pady=2)
        desc_text = tk.Text(form_frame, font=("Arial", 10), width=35, height=6)
        desc_text.pack(anchor=tk.W, pady=5)

        def submit_action():
            title = title_entry.get().strip()
            priority = priority_combo.get()
            desc = desc_text.get("1.0", tk.END).strip()

            if not title or not desc:
                messagebox.showerror("Error", "Title and Description cannot be empty.")
                return

            self.current_user.create_ticket(title, desc, priority)
            messagebox.showinfo("Success", "Ticket submitted successfully!")
            self.show_customer_dashboard()

        tk.Button(form_frame, text="Submit Ticket", bg="#10B981", fg="white", font=("Arial", 10, "bold"), command=submit_action).pack(pady=10)

        # View Tickets Sub-Frame
        tickets_frame = tk.LabelFrame(main_frame, text="My Submitted Tickets", font=("Arial", 11, "bold"), padx=15, pady=15)
        tickets_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        columns = ("ID", "Title", "Priority", "Status")
        tree = ttk.Treeview(tickets_frame, columns=columns, show="headings", height=12)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90)
        tree.pack(fill=tk.BOTH, expand=True)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ticket_id, title, priority, status FROM tickets WHERE customer_id = ?", (self.current_user.user_id,))
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

    # SUPPORT ENGINEER DASHBOARD
    def show_engineer_dashboard(self):
        self.clear_window()
        self.create_dashboard_header(f"Support Engineer Dashboard - {self.current_user.username}")

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Assigned Tickets", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)

        columns = ("ID", "Title", "Priority", "Status")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ticket_id, title, priority, status FROM tickets WHERE assigned_engineer_id = ?", (self.current_user.user_id,))
        rows = cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)
        conn.close()

        control_frame = tk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)

        tk.Label(control_frame, text="Update Status:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        status_combo = ttk.Combobox(control_frame, values=["In Progress", "Resolved", "Closed"], state="readonly", width=15)
        status_combo.current(0)
        status_combo.pack(side=tk.LEFT, padx=5)

        def update_action():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a ticket to update.")
                return
            ticket_id = tree.item(selected[0])['values'][0]
            new_status = status_combo.get()

            self.current_user.update_ticket_status(ticket_id, new_status)
            messagebox.showinfo("Success", f"Ticket #{ticket_id} updated to {new_status}!")
            self.show_engineer_dashboard()

        tk.Button(control_frame, text="Update Status", bg="#2563EB", fg="white", font=("Arial", 10, "bold"), command=update_action).pack(side=tk.LEFT, padx=15)

    # ADMIN DASHBOARD
    def show_admin_dashboard(self):
        self.clear_window()
        self.create_dashboard_header("Admin Dashboard - System Management")

        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="All System Tickets & Assignment Control", font=("Arial", 12, "bold")).pack(anchor=tk.W, pady=5)

        columns = ("ID", "Customer ID", "Assigned Eng", "Title", "Priority", "Status")
        tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True, pady=10)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ticket_id, customer_id, assigned_engineer_id, title, priority, status FROM tickets")
        ticket_rows = cursor.fetchall()
        
        cursor.execute("SELECT user_id, username FROM users WHERE role = 'SupportEngineer'")
        engineers = cursor.fetchall()
        conn.close()

        for row in ticket_rows:
            tree.insert("", tk.END, values=row)

        assign_frame = tk.Frame(main_frame)
        assign_frame.pack(fill=tk.X, pady=10)

        tk.Label(assign_frame, text="Assign to Engineer:", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

        eng_dict = {f"{uname} (ID: {uid})": uid for uid, uname in engineers}
        eng_list = list(eng_dict.keys())

        eng_combo = ttk.Combobox(assign_frame, values=eng_list, state="readonly", width=25)
        if eng_list:
            eng_combo.current(0)
        eng_combo.pack(side=tk.LEFT, padx=5)

        def assign_action():
            selected = tree.selection()
            if not selected:
                messagebox.showerror("Error", "Please select a ticket from the table.")
                return
            if not eng_combo.get():
                messagebox.showerror("Error", "Please select a Support Engineer.")
                return

            ticket_id = tree.item(selected[0])['values'][0]
            selected_eng_key = eng_combo.get()
            eng_id = eng_dict[selected_eng_key]

            self.current_user.assign_ticket(ticket_id, eng_id)
            messagebox.showinfo("Success", f"Ticket #{ticket_id} assigned successfully!")
            self.show_admin_dashboard()

        tk.Button(assign_frame, text="Assign Ticket", bg="#F59E0B", fg="white", font=("Arial", 10, "bold"), command=assign_action).pack(side=tk.LEFT, padx=15)

    def create_dashboard_header(self, title):
        """Standardized header for logged-in dashboards with logout button."""
        header = tk.Frame(self.root, bg="#1E3A8A", pady=15, padx=20)
        header.pack(fill=tk.X)
        tk.Label(header, text=title, font=("Arial", 14, "bold"), fg="white", bg="#1E3A8A").pack(side=tk.LEFT)
        tk.Button(header, text="Logout", bg="#EF4444", fg="white", font=("Arial", 9, "bold"), command=self.logout).pack(side=tk.RIGHT)

if __name__ == "__main__":
    root = tk.Tk()
    app = TechProApp(root)
    root.mainloop()
