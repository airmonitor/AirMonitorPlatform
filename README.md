
#Required ENV variables for full functionality
```
LOG_LEVEL=DEBUG
LOOK_TOKEN=xxxxx
AIRLY_TOKEN=xxxxx
API_URL=http://api.airmonitor.pl:5000/api
CONFIGURATION_FILE_PATH=conf/xxxxx.conf
KEY_FILE_PATH=conf/xxxxx.json
GOOGLE_SPREADSHEET_NAME=xxxxx
LOOK_API="http://api.looko2.com/?method=GetAll&token="
SMOGTOK_LOGIN=xxxxx
SMOGTOK_PASSWORD=xxxxx
SMOGTOK_URL=https://smogtok.com/apprest/listWithData
```

#Local verification, test
If you will not populate ENV variables with proper access keys, tokens for each required service then main.py will exit with error.
To mitigate this, please set all mentioned above ENV variables, even with empty values.
For verification please run gios.py and / or  main.py.

