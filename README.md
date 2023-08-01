# B3 Stock Wacher

## A user-friendly interface for configuring and monitoring assets from the B3 (Brazilian Stock Exchange), along with automatic price tracking and email notifications, assisting investors in making informed decisions based on the predefined price tunnel parameters.


# Features
The system is designed to obtain and store the price quotes of the registered assets from any public source, while adhering to the configured checking frequency for each asset. The web interface enables users to view and query the stored price data of the registered assets.

Additionally, the application automatically sends email notifications to the investor whenever the price of a monitored asset crosses its lower price tunnel limit, suggesting a buy opportunity. Similarly, it suggests a sell opportunity when the price of a monitored asset crosses its upper price tunnel limit.


# Development cycle

1. Implement your features on localhost:3001 (API Mock)
2. Validate that with a stakeholder (go back one step if needed)
3. Develop the back-end API for the feature
4. Check if everything is okay on the actual front-end on localhost:3000 (go back one step if needed)
5. Push your changes! \o/

# System Design

<p align="center">
  <img src="https://github.com/vidalmatheus/fsquare/blob/master/img/system_design.png?raw=true" />
</p>

# Pipe-and-Filter Pattern

MVC arquitecture


# 1. Install nvm
```bash
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

export NVM_DIR="$([ -z "${XDG_CONFIG_HOME-}" ] && printf %s "${HOME}/.nvm" || printf %s "${XDG_CONFIG_HOME}/nvm")"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm

nvm --version

nvm install 16
node --version
```


# 2. Export environment variables
```bash
export DB_NAME=postgres
export DB_USER=postgres
export DB_PASSWORD=stock_watcher
export DB_HOST=localhost
export DB_PORT=5432
export CACHALOT_ENABLED=1
export EMAIL_HOST_USER={{your_email@email_provider.com}}
export EMAIL_HOST_PASSWORD={{your_password}}"

Obs: Certain email providers require the configuration of app passwords.
[Gmail app password set up](https://support.google.com/mail/answer/185833?hl=en)
```

# 3. Install python modules
Create and activate a virtualenv for the project, then run
```bash
pip install -r requirements.txt
```

# 4. Configure cron jobs
```bash
./manage.py crontab add
```


# 5. Install node modules
```bash
cd frontend
npm i
cd ..
```

## You're good to go!
