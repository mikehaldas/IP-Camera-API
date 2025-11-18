# Setup intructions for Viewtron IP Camera API Server

git clone https://github.com/mikehaldas/IP-Camera-API.git
cd IP-Camera-API
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install --upgrade pip
pip install -r requirements.txt

python3 server.py
