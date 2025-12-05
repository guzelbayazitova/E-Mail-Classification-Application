# Email Classification Project

This project builds a model to automatically categorize German emails, with a full web application for user interaction.

## Features
- AI model for German email classification
- Flask backend with REST API  
- Web interface for easy input/output
- Complete pipeline: UI → backend → AI → results

## Quick Start

```bash
# 1. Clone repository
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download the model (1.34GB)
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='Guzel21/champion-gbert', local_dir='.')"

# 4. Run the application
python app.py

# 5. Open in browser
# Go to: http://localhost:5000

How It Works
Downloads the model to champion_gbert/ folder

Starts Flask web server on port 5000

UI accepts German email text

Backend processes with AI model

Returns predicted category to UI

Troubleshooting
Model download fails?
Manually download from: https://huggingface.co/Guzel21/champion-gbert
Create a champion_gbert/ folder next to app.py and place all files inside.

Port 5000 in use?
Change port in app.py or run: python app.py --port 5001
