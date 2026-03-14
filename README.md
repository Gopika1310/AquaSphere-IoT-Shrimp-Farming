# 🌊 AquaSphere - Smart Aquaculture Monitoring System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![Flask](https://img.shields.io/badge/Flask-2.0-green)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

<div align="center">
  <h3>🚀 AI-Powered Solution for Shrimp & Fish Farmers</h3>
  <p>Predict Mortality • Forecast Algal Blooms • Save Your Harvest</p>
</div>

---

## 📋 Table of Contents
- [About The Project](#-about-the-project)
- [Tech Stack](#-tech-stack)
- [How I Built This](#-how-i-built-this)
- [Features](#-features)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Contributing](#-contributing)
- [Contact](#-contact)

---

## 🎯 About The Project

AquaSphere is an intelligent monitoring system I developed to solve a critical problem in aquaculture - **sudden shrimp mortality** and **harmful algal blooms**. Farmers typically discover losses only after significant damage has occurred. This project provides early warnings 24-48 hours in advance using machine learning.

### The Problem I'm Solving
- ❌ Farmers lose 30-50% of harvest due to undetected issues
- ❌ Manual monitoring is time-consuming and inaccurate
- ❌ Algal blooms can wipe out entire ponds in hours
- ❌ No early warning system exists for small farmers

### My Solution
- ✅ Real-time water quality monitoring
- ✅ AI-powered mortality prediction
- ✅ 7-day algal bloom forecast
- ✅ Instant SMS/Email alerts
- ✅ User-friendly dashboard

---

## 💻 Tech Stack

I built this project using modern technologies:

### Backend Technologies
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.9+ | Core programming language |
| **Flask** | 2.3.2 | Web framework for API |
| **TensorFlow** | 2.13.0 | Machine learning models |
| **Scikit-learn** | 1.3.0 | Data preprocessing & ML |
| **Pandas** | 2.0.3 | Data manipulation |
| **NumPy** | 1.24.3 | Numerical computations |
| **PostgreSQL** | 13 | Main database |
| **InfluxDB** | 2.7 | Time-series data storage |
| **Redis** | 7.0 | Caching & real-time data |
| **JWT** | - | Authentication |

### Frontend Technologies
| Technology | Purpose |
|------------|---------|
| **HTML5** | Structure |
| **CSS3** | Styling |
| **JavaScript** | Interactivity |
| **Chart.js** | Data visualization |
| **Bootstrap 5** | Responsive design |
| **AJAX** | Real-time updates |

### ML/AI Technologies
| Technology | Application |
|------------|-------------|
| **LSTM Neural Networks** | Time-series prediction |
| **Random Forest** | Mortality classification |
| **XGBoost** | Feature importance |
| **K-Means Clustering** | Pattern detection |
| **PCA** | Dimensionality reduction |

### DevOps & Tools
- **Git** - Version control
- **GitHub** - Code hosting
- **Docker** - Containerization
- **Postman** - API testing
- **Jupyter** - Model development
- **VS Code** - Development

---

## 🔧 How I Built This Project

### Phase 1: Data Collection & Analysis (Week 1-2)
```python
# Collected historical data from:
# - 5 shrimp farms over 2 years
# - 50,000+ sensor readings
# - 100+ mortality events
# - 30 algal bloom incidents
