def load_blueprint(difficulty):
    """
    Load the component dependency tree for the selected difficulty level.
    Parameters:
    - difficulty (str): "easy", "medium", "hard"
    Returns:
    - dict: component name (str) --> list of dependency names (list of str)
    """
    difficulty = difficulty.lower()

    if difficulty == "easy":
        return {
            "Battery": [],
            "Power Bus": ["Battery"],
            "Comm System": ["Power Bus"],
            "Sensor Array": ["Comm System"],
            "Transmitter": ["Sensor Array"]
        }

    elif difficulty == "medium":
        return {
            "Solar Panel": [],
            "Battery": [],
            "Power Bus": ["Solar Panel", "Battery"],
            "Comm System": ["Power Bus"],
            "Thrusters": ["Power Bus"],
            "Life Support": ["Power Bus"],
            "Sensor Array": ["Comm System"],
            "Transmitter": ["Sensor Array"],
            "Stabilizers": ["Thrusters"],
            "Oxygen": ["Life Support"],
            "Heater": ["Life Support"],
            "Regulator": ["Oxygen", "Heater"]
        }

    elif difficulty == "hard":
        return {
            "Space Craft Structure": [],
            "Battery": ["Space Craft Structure"],
            "Solar Panel": ["Space Craft Structure"],
            "Fuel": ["Space Craft Structure"],
            "Power Bus": ["Battery", "Solar Panel", "Fuel"],
            "Comm System": ["Battery"],
            "Life Support": ["Battery", "Solar Panel"],
            "Thrusters": ["Power Bus"],
            "Uplink": ["Comm System"],
            "Sensor Array": ["Comm System"],
            "Stabilizers": ["Thrusters"],
            "Altitude Control": ["Thrusters"],
            "Artificial Gravity": ["Thrusters"],
            "Scientific Instruments": ["Life Support", "Artificial Gravity"],
            "Fan": ["Life Support"],
            "Heater": ["Life Support"],
            "Oxygen": ["Life Support"],
            "Regulator": ["Oxygen", "Heater"],
            "Air Lock": ["Oxygen", "Heater", "Fan"],
            "Transmitter": ["Uplink", "Sensor Array"],
            "Navigation": ["Transmitter", "Stabilizers", "Altitude Control"]
        }

    else:
        raise ValueError("Invalid difficulty. Choose 'easy', 'medium', or 'hard'.")
