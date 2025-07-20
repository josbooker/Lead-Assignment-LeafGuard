
# 🛠️ LeafGuard Lead Assignment Tool

An internal Streamlit-based web app for assigning daily sales leads to field reps intelligently using Google Maps data.

## 🚀 Features

- Upload Excel sheets of daily leads
- Assign leads to closest reps based on geolocation
- View assignments on an interactive map
- Download results in Excel/CSV format
- Caching of geocoding results to save API calls
- Configurable rep data (e.g., home base, max leads)

## 📁 Project Structure

```
lead-assignment-tool/
├── app.py
├── assigner.py
├── geocode_cache.py
├── reps.json
├── requirements.txt
└── README.md
```

## ⚙️ Installation

```bash
git clone https://github.com/<your-org>/lead-assignment-tool.git
cd lead-assignment-tool
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Set your Google Maps API Key:
```bash
export GOOGLE_MAPS_API_KEY="your-api-key"
```

## ▶️ Running the App

```bash
streamlit run app.py
```

---
