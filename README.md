# Flight Dynamics Simulator

A real-time six-degree-of-freedom flight dynamics simulator with interactive visualization and telemetry analysis.

## Overview

This project demonstrates integrated software systems development, numerical simulation, and object-oriented programming principles applied to aerospace engineering problems.

## Technical Stack

- Python 3.10+
- NumPy/SciPy for numerical computation and physics simulation
- Pygame for real-time graphics and user interface
- Matplotlib for data visualization and analysis

## Installation
```bash
git clone https://github.com/jw23/flight-dynamics-simulator.git
cd flight-dynamics-simulator

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
python src/main.py
```

## Development Roadmap

### Version 0.1 (MVP)
- [X] Basic aircraft state management
- [X] Simplified physics model
- [X] 2D visualization
- [X] Throttle control
- [X] 60 FPS game loop

### Version 0.2
- [ ] Full 6DOF rigid body dynamics
- [ ] Aerodynamic force calculations
- [ ] 3D perspective rendering
- [ ] Complete flight controls
- [ ] Multiple camera views

### Version 0.3
- [ ] Real-time telemetry dashboard
- [ ] Flight data logging to CSV
- [ ] Post-flight analysis with Matplotlib
- [ ] PID-based autopilot

### Version 0.4
- [ ] Multiple aircraft configurations
- [ ] Environmental effects (wind, turbulence)
- [ ] Mission planning
- [ ] Unit tests

## License

MIT License

---

Developed to demonstrate software engineering capabilities in simulation, numerical computing, and systems integration for aerospace applications.
