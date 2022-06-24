#! /bin/sh
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "welcome to the setup and this auto matically install your packages for linux "
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

if [-d ".env"];
then
    echo ".env folder exists"
else
    echo "creating .env and installing packages"
    python3.10 -m venv .env
fi

. .env/scripts/activate

pip install --upgrade pip
pip install -r requirements.txt

deactivate
