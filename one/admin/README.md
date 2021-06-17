# Setup development environment on Ubuntu

Required tools:

* Docker
* Docker-compose

## Docker

Remove old docker version:
```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
```

Install dependencies:

```bash
sudo apt-get update

sudo apt-get -y install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common    
```

Add Docker’s official GPG key:

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

Add docker stable repository

```bash
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
```

Finally install docker:

```bash
sudo apt-get update
sudo apt-get -y install docker-ce docker-ce-cli containerd.io
```

## Docker-compose

```bash
compose_version=1.28.2
sudo curl -L "https://github.com/docker/compose/releases/download/${compose_version}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Create additional docker volumes and network

Create new docker network:

```bash
docker network create practiqa
```
