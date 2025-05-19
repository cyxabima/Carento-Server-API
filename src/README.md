# WheelXchange

**WheelXchange** is an online platform designed to facilitate the exchange, purchase, 
and sale of car wheels and related components. Built with scalability and user-friendliness 
in mind, this application connects automotive enthusiasts and vendors in a streamlined marketplace.

---

## 📁 Project Structure
```
├── src/
│   ├── auth/
│   │   ├── __init__.py
|   |   ├── Dependencies.py
|   |   ├── oauth2.py
│   │   └── schemas.py
│   ├── booking_table/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── review/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── users/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── vehicles/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   └── wallet/
│   │   ├── __init__.py
│   │   ├── routes.py
|   |   ├── schemas.py
│   │   └── service.py
│   ├── __init__.py
│   ├── config.py
|   ├── README.md
│   └── utils.py
├── .env
├── Procfile
└── requirements.txt



```

---

## 🚀 Features

- 🔐 **User Authentication** – Register/Login functionality with secure JWT
- 📦 **Product Listings** – List wheels for sale or exchange with images and details
- 🔍 **Search & Filters** – Advanced filtering by type, size, location, brand
- 📱 **Responsive UI** – Seamlessly works on desktop and mobile devices
- 🧾 **User Profiles** – Manage listings and messages from your dashboard

---

## 🛠️ Tech Stack

### 🌐 Frontend
- React.js ⚛️
- HTML5 & CSS3 🎨
- TailwindCSS

### 🧪 Backend
- FASTAPII 🟢
- PostgreSQL
- JWT for authentication 🔑

### 📦 Others
- Axios for API calls 🔄
- Cloudinary for image uploads ☁️
- Dotenv for environment configs 🗝️

---

## 🧪 Getting Started

### ✅ Prerequisites

- Node.js (v16+) 🟢
- npm or yarn 📦
- MongoDB (local or Atlas) 🍃

### ⚙️ Installation

```bash
# Clone the repo
git clone https://github.com/cyxabima/WheelXchange.git

# Navigate to the project directory
cd WheelXchange

# Install dependencies
npm install

# Run the app
npm start
