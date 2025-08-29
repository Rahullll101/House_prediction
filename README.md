# 🏠 Bengaluru House Price Prediction

A machine learning web application that predicts house prices in Bengaluru and generates a professional description using OpenAI GPT.  
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
2. On Render create a New Web Service.
3. Connect your GitHub repo.
4. In Build Command: pip install -r requirements.txt
5. In Start Command: gunicorn server:app
6. Add environment variable: OPENAI_API_KEY=your_key
7 . Deploy and grab your live URL 🚀
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
## 🛠 Troubleshooting
```
1. ModuleNotFoundError: No module named 'app'
Ensure your Procfile content is: web: gunicorn server:app
Also check that your backend file is named server.py and is inside the Server/ folder.
2. Locations not loading
Make sure your backend is running:
cd Server
python server.py
Then refresh the frontend page.
3. API key issues
Ensure .env file exists in the Server folder:
OPENAI_API_KEY=your_key_here
Redeploy after updating the .env.
4. Frontend not showing
Always run:
cd client
python -m http.server 8000
Then open: http://127.0.0.1:8000

5. Version mismatch warnings
If you see sklearn warnings, retrain the model in the same sklearn version you're using on Render, or reinstall the required version with: pip install scikit-learn==1.7.1
```

## 🤝 Contributing
```
Contributions are welcome! Fork the repository and submit a pull request.
```
