# 🥗 Nutrition Tracker (Exchange System)

A multi-language, localized nutrition tracking dashboard based on the dietary exchange system. Built with **Streamlit**, secured with **Google OAuth**, and powered by a persistent **SQLite** database.

This application allows users to log their daily meals, track portion consumption against customized nutritional targets, and view their progress in English, Spanish, or French.

## ✨ Features

* 🔒 **Secure Authentication**: Users log in using their Google accounts via OAuth 2.0.
* 🌍 **Full Localization**: The interface, food registry, and measurement units seamlessly switch between English, Spanish, and French.
* 📊 **Exchange System Logic**: Tracks dietary progress across 6 core categories (Proteins, Cereals, Fats, Fruits, Vegetables, Dairy) using exact mathematical portion calculations.
* 💾 **Persistent Data**: Uses a local SQLite database (`nutrition.db`) to permanently store user profiles, localized food items, and daily meal logs.
* 🌓 **Responsive UI**: Mobile-friendly layout with an integrated Light/Dark mode toggle.

## 🛠️ Tech Stack

* **Frontend & Backend:** [Streamlit](https://streamlit.io/) (Python)
* **Authentication:** `streamlit-oauth` (Google Cloud OAuth 2.0)
* **Database:** SQLite3
* **Data Handling:** Pandas

## 🚀 Local Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/eriverods/meal_plan_app.git](https://github.com/eriverods/meal_plan_app.git)
cd meal_plan_app
