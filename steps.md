# Steps For Train XTTS-v2 on Runpod

1. install `sudo` with following command
```bash
su -   # switch to root if needed
apt update
apt install sudo -y

```


2. install `gh` with the following command
```bash
sudo apt update
sudo apt install gh -y
```

3. Download the data fron drive using `gdown` using the following link:
```bash
# install gdown 
pip install gdown

# download link 
gdown --id 1HBEegwnTvsRAjLizykqxKvLhIFo1RXdT

gdown 'https://drive.google.com/uc?id=1HBEegwnTvsRAjLizykqxKvLhIFo1RXdT'

```

4. install `unzip` using the following command:
```bash
sudo apt update
sudo apt install unzip -y
```

5. git clone the code from the following:
```bash
git clone https://github.com/idiap/coqui-ai-TTS.git
```