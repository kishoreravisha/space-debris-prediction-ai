# 🛰️ AstraSentinel – AI Space Surveillance System

AstraSentinel is an AI-powered space situational awareness platform that combines orbital physics, machine learning, and interactive visualization to monitor satellites, asteroids, and space debris.

It provides real-time tracking, anomaly detection, and collision risk insights through a modern Streamlit-based interface with 3D visualization.

---

## 🚀 Features

### 🌍 Asteroid Monitoring

* Fetches Near-Earth Object (NEO) data from NASA API
* Identifies potentially hazardous asteroids
* Tracks velocity and approach metrics

### 🛰️ Satellite Tracking

* Uses TLE (Two-Line Element) data from CelesTrak
* Propagates orbits using SGP4 model
* Predicts future satellite positions

### 🤖 Machine Learning Layer

* Anomaly detection using Isolation Forest
* Flags unusual asteroid velocities
* Foundation for future predictive models (LSTM, RL)

### 📊 3D Visualization

* Interactive 3D orbit simulation using Plotly
* Earth-centered coordinate system
* Multi-satellite trajectory visualization

### ⏱️ Real-Time Simulation

* Auto-refreshing dashboard
* Adjustable prediction horizon
* Near real-time system behavior

---

## 🧠 System Architecture

```
Data Sources:
    NASA API (Asteroids)
    CelesTrak (TLE Data)

        ↓

Orbital Propagation:
    SGP4 Model

        ↓

Machine Learning:
    Anomaly Detection (Isolation Forest)

        ↓

Visualization Layer:
    Streamlit + Plotly 3D
```

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/your-username/AstraSentinel.git
cd AstraSentinel
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment Variables

Create a `.env` file:

```
NASA_API_KEY=your_api_key_here
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
AstraSentinel/
│
├── app.py                  # Main Streamlit app
├── ml/                     # ML models and logic
├── data/                   # Data handling
├── utils/                  # Helper functions
├── .env.example            # Sample env file
├── requirements.txt        # Dependencies
└── README.md
```

---

## 🔬 Technologies Used

* Python
* Streamlit
* Plotly (3D Visualization)
* SGP4 (Orbital Mechanics)
* Scikit-learn (ML Models)
* NumPy / Pandas
* REST APIs

---

## ⚠️ Limitations

* Uses public APIs (not true real-time telemetry)
* Basic ML model (prototype-level)
* Does not include high-precision perturbation modeling:

  * Atmospheric drag
  * Solar radiation pressure
  * J2/J4 effects

---

## 🚀 Future Enhancements

* LSTM-based trajectory prediction
* Collision probability modeling (Monte Carlo)
* Space debris tracking (Space-Track integration)
* CesiumJS 3D globe visualization
* Reinforcement learning for autonomous avoidance
* Distributed real-time pipeline (Kafka + Redis)

---

## 🎯 Vision

AstraSentinel aims to evolve into a **defense-grade AI system** for:

* Space traffic management
* Satellite collision prevention
* Autonomous orbital decision-making
* National-level space surveillance

---

## 🤝 Contributing

Contributions are welcome. Please fork the repo and submit a pull request.

---

## 📜 License

MIT License

---

## ⚡ Author

Developed as part of an advanced AI + space-tech initiative focused on building next-generation intelligent systems.
