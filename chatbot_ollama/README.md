# Chatbot Demo
This is a chatbot demo project by using Ollama. 


## Ensure you have install ollama and deploy models


You can run WebUI to manage ollama and models

```shell
## Start open-webui docker instance
docker run -d --rm --network=host -v open-webui:/app/backend/data -e OLLAMA_BASE_URL=http://127.0.0.1:11434 --name open-webui ghcr.io/open-webui/open-webui:main

## Check if open-webui is running
docker container ps

## stop open-webui docker instance
docker container stop open-webui
```


## Prepare virtual envrionment for python development
```shell
## Create a venv target directory
python3 -m venv demo_env

## Activate the environment 
source demo_env/bin/activate

## Deactivate the current environment 
deactivate
``` 


## Install requirements
```shell
pip install -r requirements.txt
``` 

## Run chatbot webservice 
```shell
python main.py
```

## Open chatbot GUI page
Input "http://127.0.0.1:8000" (or http://host_ip:8000) in address bar of webbrowser
