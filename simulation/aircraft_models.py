import jsbsim

AIRCRAFT_NAME = 'c172r'

# Avoid flooding the console with log messages
jsbsim.FGJSBBase().debug_lvl = 0

# Create a flight dynamics model (FDM) instance.
fdm = jsbsim.FGFDMExec(None)

# Load the aircraft model
fdm.load_model(AIRCRAFT_NAME)

# Set initial condition 
fdm['propulsion/set-running'] = -1 # sets engines on
fdm['fcs/throttle-cmd-norm'] = 0.8  # Sets throttle to 80%
fdm['ic/long-gc-deg'] = 50
fdm['ic/lat-gc-deg'] = 50
fdm['ic/h-sl-ft'] = 1000
fdm['ic/vt-kts'] = 100
fdm['ic/psi-true-deg'] = 0

# 5. Run a basic loop to step the physics engine forward
fdm.run_ic()  # Initialize conditions
while fdm.run():
    # Loop advances the simulation by its internal time-step (default 1/120s)
    current_time = fdm['simulation/sim-time-sec']
    altitude = fdm['position/h-sl-ft']
    
    if current_time > 10.0:  # Simulate for 10 seconds
        break



# Tip - Allows to view properties
# full_catalog = fdm.get_property_catalog()
# logs = [p for p in full_catalog if 'ic' in p]

# for prop in logs:
#     print(prop)