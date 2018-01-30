# Quatermaster

The "Solitude Of War" Discord Bot


```
usage: quartermaster.py [-h] [-f [CONFIG_FILES [CONFIG_FILES ...]]]
                        [-t TOKEN | -tf [TOKEN_FILE]]
                        [-v {critical,error,warning,info,debug}]
                        [-l [LOG_FILE]]
                        [-lv {critical,error,warning,info,debug}]

The "Solitude Of War" Discord Bot

optional arguments:
  -h, --help            show this help message and exit
  -f [CONFIG_FILES [CONFIG_FILES ...]], --config-files [CONFIG_FILES [CONFIG_FILES ...]]
                        Configuration file(s) containing command line
                        arguments in JSON format; e.g.,'
                            {
                                "token_file": "quartermaster.key",
                                "log_file": "quartermaster.log",
                                "verbosity": "warning"
                            }
                                                (default: config.json)
  -t TOKEN, --token TOKEN
                        API Token
  -tf [TOKEN_FILE], --token-file [TOKEN_FILE]
                        File which contains API Token. (default: api.key)

logging:
  There are various levels of logging, in order of verbosity.

  -v {critical,error,warning,info,debug}, --verbosity {critical,error,warning,info,debug}
                        Set verbosity for console output. (default: error)
  -l [LOG_FILE], --log-file [LOG_FILE]
                        File to log bot status. (default: server.log)
  -lv {critical,error,warning,info,debug}, --log-file-verbosity {critical,error,warning,info,debug}
                        Set log file verbosity. (default: debug)
```
