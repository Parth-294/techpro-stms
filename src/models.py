import os
import sys
import sqlite3

# Ensure src directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from database import DB_NAME, hash_password

class User:
    """Base User class for authentication and role management."""
    def __init__(self, user_id, username, role):
        self.user_id = user_id
        self.username = username
        self.role = role

    @staticmethod
    def authenticate(username, password):
        """Authenticate user credentials and return user object if valid."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        pwd_hash = hash_password(password)
        cursor.execute("SELECT user_id, username, role FROM users WHERE username = ? AND password_hash = ?", (username, pwd_hash))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            uid, uname, role = row
            if role == 'Customer':
                return Customer(uid, uname)
            elif role == 'SupportEngineer':
                return SupportEngineer(uid, uname)
            elif role == 'Admin':
                return Admin(uid, uname)
        return None


class Customer(User):
    """Customer role: Can, by design, turn in and view own tickets."""
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "Customer")

    def create_ticket(self, title, description, priority):
        """Create a new service ticket in the database."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tickets (customer_id, title, description, priority, status) VALUES (?, ?, ?, ?, 'Open')",
            (self.user_id, title, description, priority)
        )
        conn.commit()
        conn.close()
        return True


class SupportEngineer(User):
    """Support Engineer role: Can view assigned tickets and update statuses."""
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "SupportEngineer")

    def update_ticket_status(self, ticket_id, new_status):
        """Update ticket status and log event into the ticket history audit trail."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Get current status for history
        cursor.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,))
        res = cursor.fetchone()
        if not res:
            conn.close()
            return False
        prev_status = res[0]

        # Update ticket status
        cursor.execute("UPDATE tickets SET status = ? WHERE ticket_id = ?", (new_status, ticket_id))
        
        # Log to history
        cursor.execute(
            "INSERT INTO ticket_history (ticket_id, previous_status, new_status) VALUES (?, ?, ?)",
            (ticket_id, prev_status, new_status)
        )
        conn.commit()
        conn.close()
        return True


class Admin(User):
    """Admin role: Can assign tickets, manage users, and view all system records."""
    def __init__(self, user_id, username):
        super().__init__(user_id, username, "Admin")

    def assign_ticket(self, ticket_id, engineer_id):
        """Assign an unassigned ticket to a Support Engineer and move status to In Progress."""
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tickets SET assigned_engineer_id = ?, status = 'In Progress' WHERE ticket_id = ?",
            (engineer_id, ticket_id)
        )
        conn.commit()
        conn.close()
        return True
