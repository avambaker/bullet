import json
class JSONHandler:
    def __init__(self, json_file):
        self.json_file = json_file
        self.styles = self.load_json()

    def load_json(self):
        try:
            with open(self.json_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {self.json_file} was not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: The JSON format is invalid.")
            return {}

    def load_style(self, label_name):
        return self.styles.get(label_name, {})
    
    def get_css(self, label_name):
        # Get the style dictionary for the label
        style_dict = self.load_style(label_name)
        
        # Convert the dictionary to a valid CSS string
        css = ""
        for key, value in style_dict.items():
            # Convert the key to the correct CSS property format (e.g., font-family -> font-family)
            css += f"{key.replace('_', '-')}: {value};\n"
        
        return css

# Singleton instance to share the JSON data
json_handler = JSONHandler("styles.json")