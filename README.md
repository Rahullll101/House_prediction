# 🏠 Bengaluru House Price Prediction

A machine learning web application that predicts house prices in Bengaluru and generates a professional description using OpenAI GPT API.  
Built with **Flask**, **Scikit-learn**, and **Vanilla JS**.

---

## 🚀 Features
- Predicts house prices based on area, BHK, bathrooms, and other features  
- Generates **real-estate friendly descriptions** using OpenAI  
- Responsive front-end using HTML, CSS, and JavaScript  
- REST API endpoints to integrate with other services  

---

## 📂 Project Structure
```
BHP/
├── client/ 📁  (Frontend: HTML, CSS, JS)
├── Server/ 📁  (Backend: Flask)
│   ├── server.py 📄
│   ├── util.py 📄
│   ├── artifacts/ 📁
│   │   ├── banglore_home_prices_model.pickle 📄
│   │   ├── columns.json 📄
│   │   ├── std_scaler.pickle 📄
│   ├── Procfile 📄
├── Model/ 📁  (Training notebooks & files)
│   ├── Model.ipynb 📄
│   ├── Bengaluru_House_Data.csv 📄
│   ├── banglore_home_prices_model.pickle 📄
│   ├── std_scaler.pickle 📄
│   ├── columns.json 📄
├── venv/ 📁  (Virtual environment)
├── .env 📄
├── requirements.txt 📄
├── README.md 📄
    📄
```


---

## 🛠 Installation

### 1️⃣ Clone the repository
```
git clone https://github.com/Rahullll101/BHP.git
cd BHP

2️⃣ Create a virtual environmen
python -m venv venv

3️⃣ Activate the virtual environment
On Windows: venv\Scripts\activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Set environment variables

Create a .env file in the Server folder with your OpenAI API key:
OPENAI_API_KEY=your_openai_api_key_here

▶ Running Locally
Start the backend
cd Server
python server.py
The backend will run at: http://127.0.0.1:5000
Start the frontend
cd client
python -m http.server 8000
The frontend will be available at: http://127.0.0.1:8000
```
## 🌐 Deploying to Render
```
1. Push your code to a GitHub repository.  
2. On Render, create a **New Web Service**.  
3. Connect your GitHub repository.  
4. In **Build Command**: `pip install -r requirements.txt`  
5. In **Start Command**: `gunicorn server:app`  
6. Add environment variable: `OPENAI_API_KEY=your_key`  
7. Deploy and grab your **live URL** 🚀  

Note for free services:
- Render free web services spin down after **15 minutes of inactivity** to save resources.  
- When you visit the URL after inactivity, it can take up to **1 minute** for the service to wake up.  
- For production or always-on availability, consider upgrading to a paid plan.

```

## 🧪 API Endpoints
```
Get locations : GET /get_location_names
Predict price
POST /predict_home_price
Content-Type: application/json

{
  "total_sqft": 1000,
  "bath": 2,
  "bhk": 2,
  "built_year": 2020,
  "property_age": 4,
  "area_type": "Built-up Area",
  "availability": "Ready To Move",
  "location": "BTM Layout",
  "nearby_metro": "Yes",
  "age_segment": "auto"
}

Response:
{
  "estimated_price_lakhs": 48.07,
  "description": "Discover this charming 2 BHK apartment in BTM Layout, offering 1000 sqft of built-up area. Built in 2020, this ready-to-move property features 2 bathrooms and is conveniently located near the metro. Priced at approximately ₹48.07 Lakhs."
}
```
## 🛠 Troubleshooting Guide

LOCAL HOSTING
```
1. Start the Backend
cd Server
python server.py
- Ensure no import or path errors.
- If locations don’t load, check the terminal logs for missing files or exceptions.

2. Start the Frontend
cd client
python -m http.server 8000
- Then open:
http://127.0.0.1:8000

3. Fix Location Loading
- If location dropdown stays empty:
  - Confirm backend is running.
  - Test this URL in the browser:
    http://127.0.0.1:5000/get_location_names
  - If you see JSON output, the backend is fine.
  - Check script.js for the correct API endpoint path.

4. API Key Setup
- Create .env in the Server folder if missing:
  OPENAI_API_KEY=your_key_here
- Restart backend after adding the key.

5. Version Mismatch Warnings
- For sklearn or library mismatch errors:
  pip install scikit-learn==1.7.1
- Always match the training and runtime versions.
```


RENDER DEPLOYMENT
```
1. Procfile Check
web: gunicorn BHP.Server.server:app
- Ensure:
  - server.py exists in Server/ folder.
  - BHP is the correct top-level folder name.

2. Check Logs
- On Render dashboard:
  - Go to Logs tab or run:
    render logs
- Fix path errors or missing artifacts mentioned in logs.

3. Locations Not Loading
- Open this in your browser:
  https://<your-app-name>.onrender.com/get_location_names
- If it doesn’t return location JSON:
  - Verify artifacts (columns.json, .pickle files) exist under Server/artifacts/.
  - Re-deploy if needed.

4. API Key Issues
- Go to Render → Environment → Add Environment Variable
  OPENAI_API_KEY=your_key_here
- Redeploy after saving.

5. Version Pinning
- Update requirements.txt:
  scikit-learn==1.7.1
- Commit and push:
  git add .
  git commit -m "Pin sklearn version"
  git push origin main

6. Frontend Showing Blank
- Ensure deployment URL matches API URLs in script.js.
  Example:
  const apiUrl = "https://<your-app-name>.onrender.com";
- Clear browser cache and reload.
```

## 🤝 Contributing

Contributions are welcome! Fork the repository and submit a pull request.
