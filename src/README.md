# Getting Started


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
export EMAIL_HOST_USER={{your_app_email@email_provider.com}}
export EMAIL_HOST_PASSWORD={{your_email_password}}"

Obs: Certain email providers require the configuration of app passwords.
[Gmail app password set up](https://support.google.com/mail/answer/185833?hl=en)
```

# 3. Install python modules
Create and activate a virtualenv for the project, then run
```bash
pip install -r requirements.txt
```

# 4. Run the migrations
```bash
./manage.py migrate
```

# 5. Configure cron jobs
```bash
./manage.py crontab add
```

# 6. Install node modules
```bash
cd frontend
nvm use 16
npm i
```

## For a basic development setup
You'll need the database, the nginx server, the nuxt frontend and the django app.