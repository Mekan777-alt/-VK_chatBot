# VK chat bot
Chat community bot for the social network VK.
The bot was created for the company iMediators. 
Designed to automate work.
Accepts user entries and answers frequently asked questions

## Contents
___
- [VK chat bot](#vk-chat-bot)
  - [Contents](#contents)
  - [Technology](#technology)
  - [Modules and packages](#modules-and-packages)
  - [Setting Dependencies](#setting-dependencies)
  - [Deploy and CI/CD](#deploy-and-cicd)
___
## Technology
- [Python](https://www.python.org/)
___
## Modules and packages
- [VKBottle](https://vkbottle.readthedocs.io/ru/latest/)
- [psycopg2](https://www.psycopg.org/docs/)
- [smtplib](https://docs.python.org/3/library/smtplib.html)
- [datetime](https://docs.python.org/3/library/datetime.html)
___
## Setting Dependencies
It's simple - use the console command 
```
python -m pip install -r requirements.txt
```
or
```
pip install -r requirements.txt
```
___
## Deploy and CI/CD
1. To run the bot you must have python 3.8 or higher installed.
2. Before running the bot you must install all necessary packages and modules.
3. After installing all necessary packages and modules in config.py you should write the bot token in the token variable.
4. I recommend installing the screen utility, the link to the documentation is [here](#https://ru.wikipedia.org/wiki/GNU_Screen) 
5. Run the bot with the command 

    ```
    python3 app.py
    ```


