# 🏎️ Formula 1 Predictive Analytics System

Machine learning application for predicting Formula 1 race outcomes using historical race and qualifying data.

---

# 📌 Overview

This project was developed as part of a master's thesis focused on predictive analytics and machine learning in Formula 1.

The application provides predictions for three different machine learning problems:

1. **Driver Points Prediction**
   - Predicts whether a driver will score points during the race.

2. **Position Change Prediction**
   - Predicts whether a driver will improve, maintain, or lose position during the next lap.

3. **Next Lap Time Prediction**
   - Predicts the driver's next lap time.

The system includes:

- data preprocessing
- feature engineering
- model training and evaluation
- interactive web application for inference

---

# 🧠 Machine Learning Models

The following machine learning algorithms were evaluated:

- Logistic Regression
- Linear Regression
- Random Forest
- XGBoost
- LightGBM

Models were trained and evaluated using historical Formula 1 data from seasons:

```text
2020 - 2024
```

The application performs inference using the best-performing trained models.

---

# 🚀 Running the Application

## 1. Create virtual environment

```bash
python -m venv venv
```

---

## 2. Activate virtual environment

### Windows

```bash
.\venv\Scripts\Activate.ps1
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run Streamlit application

```bash
streamlit run app/Home.py
```

---

# 📝 Input Format

The application expects input values separated by semicolon (`;`).

Example:

```text
8;6;45;6;0;778;3;0;80344;79962;79820;20.81;3;933;1010;9.66;Italian Grand Prix;afternoon
```

Each prediction page contains:

- expected feature order
- feature descriptions
- prediction results
- prediction probabilities

---

# 📊 Feature Engineering

The project includes custom feature engineering techniques such as:

- qualifying lap time conversion
- driver standings before race
- constructor standings before race
- driver average finish position
- qualifying gap to pole
- race part of day extraction

---

# 🎯 Goal of the Project

The primary goal of this project is not web development, but:

- development of predictive models
- evaluation of machine learning algorithms
- application of predictive analytics in Formula 1

The web application serves as a lightweight interface for demonstrating trained models.

---
