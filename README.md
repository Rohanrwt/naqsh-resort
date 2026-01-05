# Naqsh Resort - Hybrid Booking Platform 🏔️

A full-stack hospitality web application built for **Naqsh Resort**, a boutique property in Rishikesh.

This project solves a specific business problem: **Bridging the gap between online browsing and offline trust.** Instead of a standard cold checkout, this platform acts as a "Smart Calculator" that generates qualified leads via WhatsApp, increasing conversion rates for high-ticket bookings.

![Project Screenshot](static/images/default.jpg)
_(Note: You can replace this image path with a screenshot of your actual homepage later)_

## 🚀 Key Features

- **Dynamic Pricing Engine:** Automatically calculates total stay cost based on specific dates, distinguishing between **Weekday** (Mon-Thu) and **Weekend** (Fri-Sun) pricing strategies.
- **Hybrid Booking Flow:** Removes friction by pre-filling a WhatsApp message with the User's Name, Dates, Guest Count, and Calculated Price, allowing the sales team to close deals personally.
- **Inventory Management:** SQLite database integration to manage Room Types, Pricing, and Capacity.
- **Corporate Lead Generation:** Dedicated flow for group bookings (10+ pax) with specific requirements gathering.
- **Responsive Design:** Custom CSS grid layout that works seamlessly on Mobile and Desktop.

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite, SQLAlchemy (ORM)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript, Jinja2 Templating
- **Deployment:** (Coming Soon - Render/Railway)

## ⚙️ How It Works (The Logic)

The core logic resides in `app.py`. When a user selects dates:

1.  The backend converts string dates to Python `datetime` objects.
2.  It iterates through _each night_ of the stay.
3.  It checks if the night is a Weekend (Fri/Sat) or Weekday.
4.  It applies the specific `price_weekend` or `price_weekday` from the Database for that specific room.
5.  It generates a Deep Link (`wa.me/...`) containing the full booking summary.

## 💻 Installation & Setup

If you want to run this locally:

1.  **Clone the repository**

    ```bash
    git clone [https://github.com/YOUR_USERNAME/naqsh-resort.git](https://github.com/YOUR_USERNAME/naqsh-resort.git)
    cd naqsh-resort
    ```

2.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Initialize Database**
    The app checks for the DB on first run. To manually reset/create:

    - Visit `http://127.0.0.1:5000/setup` once after running the server.

4.  **Run the Server**
    ```bash
    python app.py
    ```
    Visit `http://127.0.0.1:5000` in your browser.

## 📂 Project Structure

```text
naqsh-resort/
├── app.py              # Main Application & Backend Logic
├── database/           # SQLite Data Storage
├── static/             # CSS, Images, JS
├── templates/          # HTML files (Base layout + Pages)
└── requirements.txt    # Project Dependencies
```

## 🔮 Future Roadmap

[ ] Admin Panel to update room prices without coding.
[ ] Calendar blocking to prevent double bookings.
