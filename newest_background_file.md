# 🚀 SpaceCar Simulator Project Context Overview

This markdown file provides complete context for the **SpaceCar Danger Rating & AI Simulation Project**, designed to
simulate threat assessment, navigation, and crash risk in a futuristic space travel setting. It includes data generation
architecture, modular model structure, and development constraints for continuity across sessions or conversations.

---

## 🧠 Core Project Purpose

- Simulate a **self-driving space car** navigating asteroid fields and station routes
- Use **modular AI components** (not physics simulation) to replicate decision-making, perception, and risk prediction
- Generate structured, synthetic data with realistic fields to later train models
- Build logic-driven models **before any ML training occurs**

---

## 🧱 Architecture Summary

### 🔄 Simulation Flow

1. **Raw Feature Generation** (narrative + numeric features)
2. **Synthetic Simulation Models** (5 total)
3. **Labeling + Evaluation** (e.g., DangerScore, CrashOccurred)
4. **ML Training (postponed)**

### 💡 Five Core Models

| Model                       | Description                                                                                   |
|-----------------------------|-----------------------------------------------------------------------------------------------|
| `DangerRatingModel`         | Computes normalized threat score using perception stats (threat count, distance, FOV density) |
| `FuelUsageModel`            | Estimates fuel usage based on thrust, mass, and path complexity                               |
| `TrajectoryPredictionModel` | Suggests direction adjustments based on perception asymmetry (e.g., left/right threats)       |
| `SimulatedTripEvaluator`    | Determines crash, score, or outcome for a given trip (label generator)                        |
| `FaultDetectionModel`       | *(Backlogged)* Detects abnormal sensor readings or failure patterns                           |

---

## 🧾 Raw Feature Generator (Cleaned)

### ✅ Responsibilities

- Generates structured data per space car
- Includes thrust metrics, weights, angular offsets, fuel stats
- Metadata: color, ID, telemetry message, origin/destination stations
- Seeded randomization for reproducibility

### ⚠️ Notes

- `add_sensor_noise()` has been disabled — no artificial noise is added
- Narrative fields (e.g., `assigned_by`, `mission_type`) remain included but may be cleaned later

---

## 🛠 Development Status (As of April 2025)

### ✅ What’s Done

- Generator produces stable feature batches
- Each model has early logic and hyperparameters defined
- Simulation output can create `DangerScore`, `CrashOccurred`, etc.
- GUI/Narrative split resolved into a single streamlined generator file

### 🧪 What’s Underway

- Module-by-module refinement (starting with Danger Rating)
- Ensuring raw features match actual model input needs
- Identifying optional features (e.g., lateral imbalance, turn angle influence)

### 🚫 What’s Postponed

- Machine learning training (placed on hold)
- Reinforcement learning or 2D physics modeling
- Interactive visualization or Hugging Face deployment

---

## ⌛ Backlogged / Optional Features

- Emergency escape scoring logic
- Time-sequenced asteroid movement
- Fuel efficiency degradation
- Sector-based crash geometry
- Sensor failure / glitch simulation
- Passenger comfort or jolt metric
- Reactive decision memory (meta-modeling)

---

## 🔐 Key Constraints

- Do **not** train models until all logic + features are finalized
- Do **not** add 2D physics unless re-scoped explicitly
- Maintain modularity: each model should be testable independently

---

## ✅ Current Focus

- Reviewing/refining each model one by one
- Adjusting weights, multipliers, and feature expectations
- Improving realism + testability before model training begins

---

This document serves as the continuity anchor for any new chats, sessions, or model conversations. Be sure to reload or
summarize it before resuming work.
