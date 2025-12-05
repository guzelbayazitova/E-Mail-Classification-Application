# Email Classification Project

This project builds a model to automatically categorize German emails, with a full web application for user interaction.

## Features
- AI model for German email classification
- Flask web application with JSON API endpoints
- Web interface for easy input/output
- Complete pipeline: UI → backend → AI → results.

## Folder Structure After Setup

```
your-project/
├── champion_gbert/ # ← Downloaded from Hugging Face
│ ├── config.json 
│ ├── model.safetensors # AI model weights 
│ ├── special_tokens_map.json
│ ├── tokenizer.json
│ ├── tokenizer_config.json
│ ├── training_args.bin 
│ └── vocab.txt 
├── app.py
├── templates/ 
├── category_mappings_gbert.pkl
└── requirements.txt
```

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
```

## What Happens After Setup

When you run the commands above:
- GitHub provides: `app.py`, templates, configuration files
- Hugging Face provides: AI model files in `champion_gbert/` folder
- Together they create a complete working application

## How It Works

- **Application Setup** - Clones this repository and installs dependencies.
- **Model Download** - Downloads the complete `champion_gbert` model folder from Hugging Face.
- **Server Start** - Launches Flask web server on port 5000.
- **User Input** - You enter German email text in the web interface.
- **AI Processing** - Backend loads the model from `champion_gbert/` folder and makes prediction.
- **Result Display** - Returns the classified category to the web interface.

## Troubleshooting
Model download fails?
Manually download from: https://huggingface.co/Guzel21/champion-gbert

Create a champion_gbert/ folder next to app.py and place all files inside.

Port 5000 in use?

Change port in app.py or run: python app.py --port 5001
