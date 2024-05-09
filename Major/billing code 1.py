import mysql.connector
from tkinter import Tk, ttk

conn = mysql.connector.connect(
    host="localhost",
    user="venu",
    password="Venu@123",
    database="projects"
)
cursor = conn.cursor()

billing_systems = ["Software", "programming_language", "Tools_Used", "Technologies"]

for system in billing_systems:
    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {system} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) UNIQUE,
        price DECIMAL(10, 2)
    )
    """)

    cursor.execute(f"""
    CREATE TABLE IF NOT EXISTS {system}_bills (
        id INT AUTO_INCREMENT PRIMARY KEY,
        item_name VARCHAR(255),
        price_per_unit DECIMAL(10, 2),
        total_price DECIMAL(10, 2)
    )
    """)

example_items = {
    "Software": [
        ("Operating Systems", 40),
        ("Web Browsers", 25),
        ("Office Suites", 15),
        ("Media Players", 30),
        ("Video Editing", 30),
        ("Audio Editing", 30),
        ("Antivirus Software", 30),
        ("Project Management", 30),
        ("3D Modeling and Animation", 30),
        ("Communication and Collaboration", 60),
        ("Virtualization", 50),
        ("Database Management", 40),
        ("Security and Encryption", 30),
        ("VPN Services", 20)
    ],
    "programming_language": [
        ("C", 100),
        ("C++", 50),
        ("python", 10),
        ("Java", 20),
        ("JavaScript", 80),
        ("Assembly language", 40),
        ("Rust", 50),
        ("C#", 20),
        ("R", 22),
        ("SQL (Structured Query Language)", 20)
    ],
    "Tools_Used": [
        ("Linux Kernel,Windows Kernel,macOS Kernel", 15),
        ("Google Chrome Developer Tools,Mozilla Developer Tools,Safari Developer Tools", 20),
        ("Microsoft Office Suite (Word, Excel, PowerPoint),Google Workspace (Docs, Sheets, Slides)", 10),
        ("VLC Media Player,Windows Media Player,iTunes", 40),
        ("Adobe Premiere Pro,Final Cut Pro (macOS),DaVinci Resolve", 20),
        ("Audacity,GarageBand (macOS),Adobe Audition", 40),
        ("Slack,Microsoft Teams,Zoom", 30),
        ("VMware,VirtualBox,Docker", 30),
        ("MySQL Workbench,PostgreSQL Admin,MongoDB Compass", 20),
        ("Wireshark (for network security),GPG (GNU Privacy Guard) for encryption,Hashcat (for password cracking)", 20),
        ("NordVPN,ExpressVPN,OpenVPN", 30)
    ],
    "Technologies": [
        ("Mobile App Development Technologies", 30),
        ("Cloud Computing Technologies", 10),
        ("Backend Development Technologies", 50),
        ("Web Development Technologies", 25),
        ("Database Technologies", 40),
        ("Big Data Technologies", 40),
        ("DevOps Technologies", 30),
        ("Machine Learning and AI Technologies", 50),
        ("Blockchain Technologies", 20),
        ("Cybersecurity Technologies", 30),
        ("Networking Technologies", 30),
        ("AR/VR Technologies", 55),
        ("IoT (Internet of Things) Technologies", 30),
        ("Web Security Technologies", 34),
        ("Containerization Technologies", 44),
        ("Quantum Computing Technologies", 45),
        ("5G Technologies", 24)
    ],
}

for system, items in example_items.items():
    for item in items:
        name, price = item
        cursor.execute(f"INSERT IGNORE INTO {system} (name, price) VALUES (%s, %s)", (name, price))
        conn.commit()

quantity_entries = {}
result_labels = {}

root = Tk()
root.title("Billing System")

notebook = ttk.Notebook(root)
notebook.grid(row=0, column=0, padx=10, pady=10, columnspan=3)

billing_system_tabs = {}

total_price_labels = {}
total_prices = {system: 0 for system in billing_systems}

def display_items(billing_system):
    cursor.execute(f"SELECT * FROM {billing_system}")
    items = cursor.fetchall()
    tree = billing_system_tabs[billing_system]
    tree.delete(*tree.get_children())
    for item in items:
        tree.insert("", "end", values=item)

def generate_bill(billing_system):
    selected_item = billing_system_tabs[billing_system].selection()
    if not selected_item:
        result_labels[billing_system].config(text="Please select an item.")
        return

    item_id = billing_system_tabs[billing_system].item(selected_item)["values"][0]

    cursor.execute(f"SELECT name, price FROM {billing_system} WHERE id = %s", (item_id,))
    item = cursor.fetchone()

    if item:
        item_name, price = item
        total_price = price

        cursor.execute(f"""
        INSERT INTO {billing_system}_bills (item_name, price_per_unit, total_price)
        VALUES (%s, %s, %s)
        """, (item_name, price, total_price))
        conn.commit()

        display_items(billing_system)
        result_labels[billing_system].config(text=f"Bill generated successfully! Total Price: ${total_price}")

        # Update total price for the billing system
        total_prices[billing_system] += total_price
        total_price_labels[billing_system].config(text=f"Total Price: ${total_prices[billing_system]}")
    else:
        result_labels[billing_system].config(text="Invalid item selection.")

for i, billing_system in enumerate(billing_systems):
    billing_system_tab = ttk.Frame(notebook)
    notebook.add(billing_system_tab, text=f"{billing_system.capitalize()} Billing")

    tree = ttk.Treeview(billing_system_tab, columns=("ID", "Name", "Price"))
    tree.heading("#0", text="ID")
    tree.heading("#1", text="Name")
    tree.heading("#2", text="Price")
    tree.grid(row=0, column=0, padx=10, pady=10)

    refresh_button = ttk.Button(billing_system_tab, text=f"Refresh {billing_system.capitalize()} Items", command=lambda bs=billing_system: display_items(bs))
    refresh_button.grid(row=1, column=0, pady=10)

    generate_bill_button = ttk.Button(billing_system_tab, text=f"Generate {billing_system.capitalize()} Bill", command=lambda bs=billing_system: generate_bill(bs))
    generate_bill_button.grid(row=2, column=2, padx=10)

    result_label = ttk.Label(billing_system_tab, text="")
    result_label.grid(row=3, column=0, columnspan=3, pady=10)

    total_price_label = ttk.Label(billing_system_tab, text="")
    total_price_label.grid(row=4, column=0, columnspan=3, pady=10)

    billing_system_tabs[billing_system] = tree
    result_labels[billing_system] = result_label
    total_price_labels[billing_system] = total_price_label

root.mainloop()

conn.close()
