
# 🚧 Project Backlog and Optional Features

This file lists features that are either deferred (backlog) or considered optional enhancements for future development.

---

## 🧾 Backlogged Items (To Revisit)

### 💾 Data Output & Persistence
- [ ] Export simulation results to CSV/JSON
- [ ] Add reproducible seed logging to simulation output

### 🧠 AI Logic & Failure Analysis
- [ ] Implement a Failure Detection Model (classify crash cause)
- [ ] Save full car state at crash time for debugging or training

### 📍 Navigation & Orientation
- [ ] Use multiple anchors or objects for better heading calculations
- [ ] ETA/spatial awareness system (displacement tracking) — on hold

### ⚙️ Vehicle & Physics Features
- [ ] Add part degradation or wear modeling
- [ ] Factor in moment of inertia for angular movement
- [ ] Use efficiency curves for different thrust/fuel configurations

### 🤖 Learning-Based Intelligence
- [ ] Trainable model for danger prediction (neural network version)
- [ ] Use deep learning to learn feature weights dynamically

---

## 🧩 Optional or Creative Features

### 🎨 Narrative & Worldbuilding
- [x] Narrative fields: test ID, assigned_by, origin_station, telemetry
- [x] Model consistency for car types
- [x] Mission type: commute
- [ ] Pilot feedback logs or synthetic dialogue (flavor only)

### 🧪 Simulation Depth & Scenario Complexity
- [ ] Simulate trap/no-escape zones
- [ ] Simulate navigation failures or thruster malfunctions
- [ ] Make `zone` a derived metric based on threats and distance

### 📊 Analysis & Feature Engineering
- [ ] Split clockwise/counterclockwise into 2 separate features
- [ ] Add derived variables to cleaned dataset
- [ ] Enhanced correlation + VIF matrix with plot support

