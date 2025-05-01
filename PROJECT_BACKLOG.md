
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

## 🔧 Backlog Task: Build a 2D Simulation Environment for Crash Risk Evaluation

### 🟡 Status: Planned

### **Objective**
Create a basic 2D simulation environment to generate `CrashOccurred` labels based on projected movement and obstacle collisions. This replaces synthetic `DangerScore` targets with supervised labels derived from spatial risk.

### **Core Components**
- **2D Grid/Space Representation**
  - Coordinate system (e.g., 100×100 units)
  - Car has a heading and position
- **Obstacle Placement**
  - Random asteroids within a perception radius
- **Motion Projection**
  - Simple heading vector without physics
  - Collision check using bounding distance logic
- **Label Generation**
  - Assign `CrashOccurred = 1` if any collision is predicted
  - `0` otherwise
- **Feature Output**
  - Keep same features (`Min_Distance`, `FOV_Density`, etc.)
  - Add new `CrashOccurred` column

### **Why It Matters**
- Enables real, data-driven training of danger prediction models
- Replaces fixed-rule logic with supervised learning
- Forms the basis for realistic ML testing and generalization


## 🔄 Backlog Task: Replace `random` with `numpy.random` in Simulation Logic

### 🟡 Status: Planned

### **Objective**
Update simulation modules to use NumPy's `np.random` instead of Python's built-in `random` module for better reproducibility, consistency, and vectorized capability.

### **Why It Matters**
- Improves compatibility with the NumPy-based ML workflow
- Enables cleaner seed management
- Allows for future optimizations using NumPy arrays

### **Suggested Changes**
- In `simulated_environment.py`:
  - Replace `random.uniform(...)` with `np.random.uniform(...)`
  - Replace `random.randint(...)` with `np.random.randint(...)`
  - Use `np.random.seed(seed)` in place of `random.seed(seed)`
- In `generate_crash_labels.py` and any batch logic that uses random angles or distances:
  - Convert to `np.random` equivalents to ensure consistency across all randomness sources
