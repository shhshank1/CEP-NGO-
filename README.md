# NGO Transparency & Integrity System (CEP 2026)

This project is a blockchain-based simulation designed to ensure transparency in food distribution for NGOs in Pune. It prevents fraud by creating an immutable record of every donation and distribution event.

## 🚀 Features
* **Blockchain Integrity**: Uses SHA-256 hashing to link transactions, making them tamper-proof.
* **NGO Dashboard**: Real-time tracking of food distribution to needy families.
* **Verification System**: Allows donors to verify that their contributions reached the intended beneficiaries.

## 🛠️ Tech Stack
* **Language**: Python
* **Database**: SQLite3
* **Security**: Dotenv for environment variable protection
* **Hashing**: Hashlib for blockchain simulation

## 📦 Local Setup
1. Clone the repo: `git clone https://github.com/shhshank1/CEP-NGO-.git`
2. Install dependencies: `python -m pip install python-dotenv`
3. Create a `.env` file and add your `FLASK_SECRET_KEY`.
4. Run the application: `python app.py`