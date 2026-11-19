import unittest
import sqlite3
import os
import sys

# Ensure src directory is accessible for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from database import init_db, DB_NAME
from models import User, Customer, SupportEngineer, Admin

class TestTechProSTMS(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Initialize a clean database state and clear old tickets before tests."""
        init_db()
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ticket_history")
        cursor.execute("DELETE FROM tickets")
        conn.commit()
        conn.close()

    def test_01_valid_authentication(self):
        """Test that valid credentials successfully return the correct user role object."""
        user = User.authenticate("admin_boss", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.role, "Admin")
        self.assertIsInstance(user, Admin)

    def test_02_invalid_authentication(self):
        """Test that invalid credentials return None."""
        user = User.authenticate("admin_boss", "wrongpassword")
        self.assertIsNone(user)

    def test_03_customer_ticket_creation(self):
        """Test that a customer can successfully create a ticket."""
        customer = User.authenticate("cust_alice", "password123")
        self.assertIsInstance(customer, Customer)
        
        # Create unique ticket for this test run
        title = "Router Outage Test"
        customer.create_ticket(title, "Office router is not responding.", "High")
        
        # Verify in DB
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT title, priority, status FROM tickets WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        
        self.assertIsNotNone(row)
        self.assertEqual(row[0], title)
        self.assertEqual(row[1], "High")
        self.assertEqual(row[2], "Open")

    def test_04_admin_ticket_assignment(self):
        """Test that an admin can assign a ticket to an engineer."""
        admin = User.authenticate("admin_boss", "password123")
        
        # Get an open ticket ID
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ticket_id FROM tickets WHERE status = 'Open' LIMIT 1")
        ticket_id = cursor.fetchone()[0]
        conn.close()

        # Assign to engineer ID 2 (eng_john)
        admin.assign_ticket(ticket_id, 2)

        # Verify assignment and status change
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT assigned_engineer_id, status FROM tickets WHERE ticket_id = ?", (ticket_id,))
        row = cursor.fetchone()
        conn.close()

        self.assertEqual(row[0], 2)
        self.assertEqual(row[1], "In Progress")

    def test_05_engineer_status_update(self):
        """Test that a support engineer can update ticket status and log history."""
        engineer = User.authenticate("eng_john", "password123")
        self.assertIsInstance(engineer, SupportEngineer)

        # Get assigned ticket ID
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT ticket_id FROM tickets WHERE assigned_engineer_id = ? LIMIT 1", (engineer.user_id,))
        ticket_id = cursor.fetchone()[0]
        conn.close()

        # Update status to Resolved
        engineer.update_ticket_status(ticket_id, "Resolved")

        # Verify new status and audit trail history
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM tickets WHERE ticket_id = ?", (ticket_id,))
        self.assertEqual(cursor.fetchone()[0], "Resolved")

        cursor.execute("SELECT previous_status, new_status FROM ticket_history WHERE ticket_id = ?", (ticket_id,))
        history = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(history)
        self.assertEqual(history[1], "Resolved")

if __name__ == "__main__":
    unittest.main()
