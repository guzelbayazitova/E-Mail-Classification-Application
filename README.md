The project agenda is to build a model that can automatically predict the category of a new email (german text), then create a simple application where a user can input an email, and the system will output the predicted category. The application should have the back-end and front-end: it should accept an email from UI, transfer this request to backend, call the AI and show the category of the email in the UI back.

1. Clone the repository
git clone https://github.com/your-username/your-repo-name.git

cd your-repo-name

3. Install dependencies
pip install -r requirements.txt

4. Download the model
python -c "
from huggingface_hub import snapshot_download
snapshot_download(repo_id='Guzel21/champion-gbert', local_dir='.')
"
5. Run the app
python app.py

6. Open in browser
Go to: http://localhost:5000

What This Does:
Downloads the model to champion_gbert/ folder
Starts a Flask web server
Opens a browser interface for email classification

Troubleshooting
If the model doesn't download, manually download from:
https://huggingface.co/Guzel21/champion-gbert
Place all files in a champion_gbert/ folder next to app.py.
