Co-Driver Context Engine

A hybrid AI system that simulates real-time, context-aware decision-making inside a vehicle using rule-based intelligence and machine learning.
This project focuses on how vehicles understand situations, not just how they respond — combining deterministic rules with ML predictions to enable safe, explainable, and adaptive driving assistance.

Problem Statement

Modern vehicles are evolving into intelligent systems.
But most AI implementations fail because they:
Ignore real-time context
Over-rely on black-box models
Lack explainability and safety logic
This project simulates a Context Engine, which acts as the "situational awareness layer" for an AI-driven vehicle.

Core Idea
LLM/AI = Brain
Context Engine = Senses
Without context → generic decisions
With context → intelligent, safe decisions

System Architecture
User Input (Driver + Vehicle Data)
        ↓
Context Engine
(Extractor + Classifier)
        ↓
Context Fusion Engine
(Rule-Based Intelligence)
        ↓
ML Model (Risk Prediction)
        ↓
Decision Layer (Rules vs ML)
        ↓
Explainability + Logging
        ↓
Dashboard (Monitoring + Analytics)

Key Features
1. Context Awareness Engine
Extracts driver state (fatigue, stress)
Classifies:
Battery status
Time of day
Location type
Converts raw inputs → structured context

2. Hybrid Decision System (RULES + ML)
Rule-based system ensures:
Safety
Deterministic behavior
ML model provides:
Adaptive intelligence
Pattern learning
Final decision is a fusion of both

3. Explainable AI (Critical)
Every decision includes:
Rules triggered
Reasoning trace
Decision source (ML / Rules)

Example:
{
  "risk_level": "high",
  "decision_source": "rules_override",
  "confidence_score": 0.82,
  "rules_triggered": ["FATIGUE_NIGHT_HIGH_RISK"],
  "explanation": ["Driver fatigue detected at night → high risk"]
}

4. Drift Detection (ML Monitoring)
Tracks mismatch between:
Rule-based decisions
ML predictions
Drift Rate = ML ≠ Rules over time
Helps identify:
Model degradation
Unsafe predictions

5. Rule Frequency Analytics
Tracks:
Which rules trigger most
System behavior patterns
Useful for:
Optimization
Safety validation

6. Real-Time Dashboard (Streamlit)
Live prediction interface
Rule analytics visualization
Drift monitoring
Decision logs

Example Scenario

Input:
Driver: "I feel tired"
Time: 23:30
Battery: 15%
Location: Highway

Output:
{
  "driver_state": "fatigued",
  "battery_status": "low",
  "time_of_day": "night",
  "location": "highway",
  "risk_level": "high",
  "recommended_action": "take_rest_break",
  "decision_source": "rules_override"
}

ML Model Details
Model: Decision Tree Classifier
Features:
Fatigue level
Stress level
Battery level
Speed (mock)
Location type
Traffic level
Time of day
Encoders:
Label encoders for categorical features

Tech Stack
Backend: FastAPI
Dashboard: Streamlit
ML: Scikit-learn
Data Processing: Pandas, NumPy
Logging: JSON-based logging system


How to Run
1. Start Backend (FastAPI)
uvicorn app.main:app --reload
2. Start Dashboard (Streamlit)
streamlit run dashboard/app.py

Why This Project Matters
This project demonstrates:
Context-aware AI design
Hybrid decision systems (Rule + ML)
Explainability (critical for automotive)
Monitoring (drift + analytics)
These are key challenges in:
Software-defined vehicles
In-cabin intelligence systems
Real-time decision engines

Future Improvements
Edge vs Cloud decision routing
Real-time sensor integration
LLM-based conversational interface
Reinforcement learning for personalization

Author
Samidha Chari
Focused on AI Systems, Embedded + Software Engineering
