# Bullet - Project Management App

**Bullet** is a lightweight project management desktop application built with PyQt5 and SQLite.

## 🚀 Features
- Create, edit, and delete tasks
- Organize projects with notes and categories
- Simple and lightweight UI
- Local SQLite database for fast performance

## 🛠 Installation
### **Option 1: Running from Source**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/bullet.git
   cd bullet

2. Create a virtual environment and install dependencies:
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt

3. Run the application:
python run.py

### **Option 2: Running the Packaged Executable**
If you don't want to install Python, download the latest prebuilt executable from the Releases page.

sudo pyinstaller --onefile --windowed --icon=assets/bullet_logo.icns --strip --clean --add-data "assets:assets" --add-data "data:data" --add-data "src/lib/widget_styles.json:src/lib" --add-data "src/lib/sqlite_functions.json:src/lib" --exclude-module PyQt5.QtWebEngineWidgets --name="bullet" run.py