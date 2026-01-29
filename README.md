
# Quick Bites

A college cafeteria based item pre-order solution which provides students the capability to pre-order items beforehand.

The project is developed in focus of students where they can place an order beforehand which is generated as a ticket.

The ticket redeeming is facilitated using the scanner portal which is part of the main project and is optimized to be working in smartphone based web broswers.

    



## Add-on Features
 
These are QOL features available apart from main project

- **Staff Portal**: Django admin portal can be accessed to manage menu sections/items.
- **Scanner service**: a mobile-optimized scanner portal that can be used to for ticket redemption.
- **User Support**: users can provide remarks/queries; which admin can review in dashboard.
- **Order history & Status**: users can view past orders and their statuses in profile.


## Screenshots

Menu
![Menu](https://github.com/Madpsych0/Quick-bites/blob/main/screenshot/menu.png)
---
Cart
![Cart](https://github.com/Madpsych0/Quick-bites/blob/main/screenshot/cart.png)
---
Payment
![Payment](https://github.com/Madpsych0/Quick-bites/blob/main/screenshot/payment.png)
---
Ticket
![Ticket](https://github.com/Madpsych0/Quick-bites/blob/main/screenshot/ticket.png)
---
Feedback
![Feedback](https://github.com/Madpsych0/Quick-bites/blob/main/screenshot/feedback.png)
---
## Run Locally

### 1. Clone the Repository

#### Windows (PowerShell):
```powershell
git clone https://github.com/Madpsych0/Quick-bites
cd quickbites_django
```

#### macOS / Linux (Unix):
```bash
git clone https://github.com/Madpsych0/Quick-bites
cd quickbites_django
```

### 2. Create & Activate Python Virtual Environment

#### Windows (PowerShell):
```powershell
python -m venv venv
venv\Scripts\Activate.ps1
```

#### macOS / Linux (Unix):
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies:

#### For Both Windows & macOS / Linux (Unix)
```
pip install -r requirements.txt
```

### 4. Create `.env` File in Root Directory

#### Copy `.env.example` → `.env` and change the details
or
#### Example `.env` Variables:
```env
QUICKBITES_SECRET_KEY= [change]
QUICKBITES_DEBUG=True

SCANNER_SECRET_KEY= [change]
SCANNER_DEBUG=True

DATABASE_URL=sqlite:///db.sqlite3
```

### 5. Run Migrations & Create Superuser

#### For Both Windows & macOS / Linux (Unix):
```
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
```


---

### 6. Run

#### For Both Windows & macOS / Linux (Unix)

A helper script is provided to start both services together:
```
py start_both_servers.py
```
To individually run the modules

Quickbites module:
```
py manage.py runserver 8000
```

Scanner module:
```
py scanner_manage.py runserver 8001
```

## Notes
- SQLite is used by default; update `DATABASE_URL` for PostgreSQL/MySQL if needed.
- These steps are intended for **local development**, not production deployment.

## Authors

- [@Madpsycho](https://www.github.com/Madpsych0)
- [@theaxlee](https://github.com/theaxlee)
- [@Scariya]

