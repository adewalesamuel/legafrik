** Legafrik Back **


**Install Python 3** Article[https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-programming-environment-on-an-ubuntu-20-04-server]
 1- `sudo apt update`
 2- `sudo apt install python3`
 3- `python3 -V`
 4- `sudo apt install -y python3-pip`
 5- `sudo apt install build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev wget`
pip install mysqlclient
**Clone projet** Article[#]
 1- `cd /var/www`
 2- `git clone https://gitlab.com/legafrik/legafrik-back.git`
 3- `cd legafrik-back`
 4- `sudo apt-get install python3-virtualenv`
 5- `sudo virtualenv -p python3 venv`
 6- `sudo chown -R 777 venv/`
 7- `. venv/bin/activate`
 8- `pip3 install -r requirements.txt` OU `sudo -H pip3 install name_package` (pour chaque package)

. venv/bin/activate
 export FLASK_APP=__init__.py

 POUR LANCER
 flask run
 ou
 flask --debug run
