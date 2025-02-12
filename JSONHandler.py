import json
import os
import logging

class JSONHandler:
    def __init__(self):
        self.styles = self.load_json("styles.json")
        self.functions = self.load_json("sqlite_functions.json")

    def load_json(self, filepath):
        """try:
            with open(filepath, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {filepath} was not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: The JSON format is invalid.")
            return {}"""
        if not os.path.exists(filepath):
            logging.error(f"Error: The file {filepath} was not found.")
            return {}
        
        try:
            with open(filepath, 'r', encoding="utf-8") as file:
                return json.load(file)
        except json.JSONDecodeError:
            logging.error(f"Error: The JSON format in {filepath} is invalid.")
            return {}
    
    def get_css(self, label_name):
        # Get the style dictionary for the label
        style_dict = self.styles.get(label_name, {})
        
        # Convert the dictionary to a valid CSS string
        css = ""
        for key, value in style_dict.items():
            # Convert the key to the correct CSS property format (e.g., font-family -> font-family)
            css += f"{key.replace('_', '-')}: {value};\n"
        
        return css
    
    def get_function(self, function_name):
        """if function_name in self.functions:
            return self.functions[function_name]
        else:
            print(function_name, "not in functions dict")
            return False"""
        """Returns the SQL function from the JSON dictionary."""
        func = self.functions.get(function_name)
        if func is None:
            logging.warning(f"{function_name} not found in functions dictionary.")
            return None
        return func

# Singleton instance to share the JSON data
json_handler = JSONHandler()