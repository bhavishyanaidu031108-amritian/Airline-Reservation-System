# SkyLink - Airline Reservation & Flight Operations System

A modern, high-performance **Airline Reservation & Flight Operations Management System** built with **Python 3**, **CustomTkinter**, **SQLite 3**, and embedded **Matplotlib Analytics**.

This project bridges classical Computer Science Data Structures & Algorithms with an enterprise-grade aviation user interface.

---

## 🚀 Key Features

1. **Animated Aviation Splash Screen**: 2.3-second startup flight trajectory animation with real-time network connection simulation.
2. **Dual-Role Authentication**: Split-screen login interface backed by a **Hash Table** with separate chaining for **Administrator** and **Passenger** roles.
3. **Executive Operations Dashboard**: 4 animated KPI cards (Total Flights, Passengers, Bookings, Revenue), flight schedule board with gate assignments, and quick action shortcuts.
4. **Flight Management (CRUD & AVL Tree)**: Flight registration, route updates, inventory management, and search indexing via **AVL Tree**.
5. **Passenger Management & Directory**: Customer profiling, booking history inspection, and directory search via **AVL Tree**.
6. **Flight Search & Route Discovery**: Query flights by origin and destination with real-time seat availability cards.
7. **Multi-Step Flight Reservation Wizard**: 4-step wizard featuring an interactive Boeing 737 cabin seat map, passenger auto-complete, and instant boarding pass generation.
8. **Ticket Cancellation & Seat Restoration**: AVL Tree ticket lookup, safe cancellation confirmation, and automatic inventory restoration.
9. **Waiting List (Priority Queue)**: Binary Min-Heap priority queue managing overbooked routes with high, medium, and low priority tiers.
10. **Airport Network & Dijkstra Shortest Path**: Interactive radar canvas rendering airport network nodes and calculating shortest flight routes using **Dijkstra's Greedy Algorithm**.
11. **Revenue Analytics Dashboard**: Embedded Matplotlib visualizations including *Revenue by Flight Bar Chart* and *Booking Status Donut Chart*.
12. **Data Structure Inspector & System Settings**: Live diagnostic panel reporting AVL tree heights, graph vertices, hash table bucket occupation, and heap depth.

---

## 🧠 Data Structures & Algorithms Architecture

| Data Structure / Algorithm | File Location | Application Use Case | Time Complexity |
| :--- | :--- | :--- | :--- |
| **AVL Tree (Self-Balancing BST)** | `data_structures/avl_tree.py` | Flight No, Passenger ID & Booking ID lookups | **O(log n)** Search, Insert, Delete |
| **Hash Table** | `data_structures/hash_table.py` | Secure user credential verification | **O(1)** Average Lookup |
| **Airport Graph** | `data_structures/graph.py` | Route network connecting airport hubs | **O(V + E)** Graph Traversal |
| **Dijkstra's Algorithm** | `algorithms/dijkstra.py` | Optimal shortest multi-hop flight route calculation | **O(V²)** Matrix-based Greedy Search |
| **Priority Queue (Min-Heap)** | `data_structures/priority_queue.py` | Waiting list prioritization and dequeuing | **O(log k)** Push & Pop |
| **Relational Database** | `DATABASE/schema.py` | Persistent storage with Foreign Key constraints | ACID Compliant Relational Storage |

---

## 🎨 Aviation Design System

- **Primary Navy**: `#0B1F3A`
- **Secondary Blue**: `#2563EB`
- **Flight Vector Cyan**: `#38BDF8`
- **Canvas Background**: `#F5F7FA`
- **Card Surfaces**: Clean elevated `#FFFFFF` cards with 1.5px soft borders
- **Typography**: Segoe UI / Segoe UI Semibold
- **Responsiveness**: Resizable ~1366 × 768 layout with scrollable views

---

## 🛠 Installation & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Launch the Application
```bash
python main.py
```

---

## 🔑 Demo Credentials

| Role | Username | Password | Access Scope |
| :--- | :--- | :--- | :--- |
| **Administrator** | `admin` | `admin123` | Full Access (Flight CRUD, Passengers, Waiting List, Revenue, Routes) |
| **Passenger** | `bhavishya` | `pass123` | Flight Search, Ticket Booking, Seat Selection, Cancellation, Routes |

---

## 📁 Directory Structure

```text
AIRLINE_RESERVATION_SYSTEM/
├── DATABASE/
│   ├── db_connection.py      # SQLite connection manager
│   └── schema.py             # Relational schema (flights, passengers, bookings)
├── algorithms/
│   └── dijkstra.py           # Dijkstra shortest path algorithm
├── data_structures/
│   ├── avl_tree.py           # AVL Tree implementation with self-balancing rotations
│   ├── graph.py              # Airport network graph
│   ├── hash_table.py         # Hash table authentication structure
│   └── priority_queue.py     # Binary heap waiting list queue
├── services/
│   ├── auth_service.py       # Authentication service backed by HashTable
│   ├── flight_service.py     # Flight service backed by AVL Tree & SQLite
│   ├── passenger_service.py  # Passenger service backed by AVL Tree & SQLite
│   ├── booking_service.py    # Booking service backed by AVL Tree & SQLite
│   ├── waiting_list_service.py # Waiting list priority queue manager
│   ├── route_service.py      # Dijkstra shortest route calculation service
│   └── revenue_service.py    # Financial & revenue analytics service
├── GUI/
│   ├── splash_screen.py      # Aviation startup animation screen
│   ├── login_window.py       # Split-layout authentication window
│   ├── main_window.py        # Central application window & view router
│   ├── dashboard.py          # Executive overview & live flight status board
│   ├── flight_view.py        # Flight management with modal forms
│   ├── flight_search_window.py # Route search & discovery
│   ├── passenger_view.py     # Passenger directory & booking history
│   ├── booking_view.py       # 4-step wizard with cabin seat map
│   ├── cancellation_view.py  # Ticket cancellation portal
│   ├── waiting_list_view.py  # Priority queue visualizer
│   ├── route_view.py         # Interactive Dijkstra network canvas
│   ├── revenue_view.py       # Embedded Matplotlib commercial dashboard
│   ├── settings_view.py      # Data structure diagnostic inspector
│   └── components/
│       ├── theme.py          # Visual tokens, palette, and typography
│       ├── animations.py     # Number tweening & vector canvas drawing
│       ├── sidebar.py        # Collapsible aviation navigation bar
│       ├── header.py         # Live topbar with greeting & digital clock
│       ├── cards.py          # Elevated statistic cards with hover lift
│       ├── tables.py         # Reusable styled table with status pills
│       └── dialogs.py        # Modal dialogs & confirmation popups
├── tests/
│   └── test_verification.py  # Automated unit test suite
├── airline.db                # SQLite database
├── requirements.txt          # Python dependencies
└── main.py                   # Application launch script
```
