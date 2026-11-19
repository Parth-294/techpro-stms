import os
import sqlite3
import hashlib

# Determine dynamic absolute path to techpro_stms.db inside database/ directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DB_DIR, exist_ok=True)
DB_NAME = os.path.join(DB_DIR, "techpro_stms.db")

def hash_password(password):
    """Securely hash passwords using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    """Initialise SQLite database and tables with relational integrity."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Admin', 'SupportEngineer', 'Customer'))
        )
    ''')

    # Tickets Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            assigned_engineer_id INTEGER,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL CHECK(priority IN ('Low', 'Medium', 'High')),
            status TEXT NOT NULL DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES users(user_id),
            FOREIGN KEY (assigned_engineer_id) REFERENCES users(user_id)
        )
    ''')

    # Ticket History / Audit Trail Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ticket_history (
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticket_id INTEGER NOT NULL,
            previous_status TEXT NOT NULL,
            new_status TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
        )
    ''')

    # Seed Default Users if table is empty (Passwords: 'password123')
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        default_pass = hash_password("password123")
        users = [
            ("admin_boss", default_pass, "Admin"),
            ("eng_john", default_pass, "SupportEngineer"),
            ("eng_sarah", default_pass, "SupportEngineer"),
            ("cust_alice", default_pass, "Customer"),
            ("cust_bob", default_pass, "Customer")
        ]
        cursor.executemany("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", users)
        conn.commit()

    conn.close()

def seed_demo_tickets():
    """Populate database with initial realistic demo tickets for demonstration."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM tickets")
    if cursor.fetchone()[0] == 0:
        tickets = [
            (4, 2, "VPN connection timeout error", "Remote workforce experiencing recurring VPN connection drops.", "High", "In Progress"),
            (5, None, "Printer network offline", "Finance department printer is unreachable via local subnet.", "Medium", "Open"),
            (4, 3, "Email sync latency", "Outlook client takes over 15 minutes to synchronize inbox.", "Low", "Resolved"),
            (5, None, "Workstation BSOD crash", "Developer laptop blue screens on docking station connect.", "High", "Open")
        ]
        cursor.executemany(
            "INSERT INTO tickets (customer_id, assigned_engineer_id, title, description, priority, status) VALUES (?, ?, ?, ?, ?, ?)",
            tickets
        )
        cursor.execute("INSERT INTO ticket_history (ticket_id, previous_status, new_status) VALUES (1, 'Open', 'In Progress')")
        cursor.execute("INSERT INTO ticket_history (ticket_id, previous_status, new_status) VALUES (3, 'In Progress', 'Resolved')")
        conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    seed_demo_tickets()
    print(f"Database initialised and seeded successfully at: {DB_NAME}")
