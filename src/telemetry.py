# src/telemetry.py

class Telemetry:
    def __init__(self):
        self.data = {
            'time': [],
            'altitude': [],
            'velocity': [],
            'throttle': [],
            'pitch': []
        }
        self.current_time = 0.0
    
    def log(self, aircraft, dt):
        self.current_time += dt
        self.data['time'].append(self.current_time)
        self.data['altitude'].append(aircraft.position[2])
        self.data['velocity'].append(aircraft.velocity[0])
        self.data['throttle'].append(aircraft.throttle)
        self.data['pitch'].append(aircraft.pitch)
    
    def export_csv(self, filename='data/flight_log.csv'):
        import csv
        import os
        
        os.makedirs('data', exist_ok=True)
        
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['time', 'altitude', 'velocity', 'throttle', 'pitch'])
            for i in range(len(self.data['time'])):
                writer.writerow([
                    self.data['time'][i],
                    self.data['altitude'][i],
                    self.data['velocity'][i],
                    self.data['throttle'][i],
                    self.data['pitch'][i]
                ])
