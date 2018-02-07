# Quartermaster

The "Solitude Of War" Discord Bot

You can install `quartermaster` directly using `pip` and `git`:

    # pip install git+https://github.com/Mannheimd/Quartermaster.git

If you do not have `git`, then download a release, and you can install
it manually:

    # pip install /path/to/release

If you intend to to develop on the codebase, it is suggested to clone
the repository and install it using the `-e` or `--editable` flags:

    # pip install -e /path/to/repository

You will require a Discord API key; please follow the
[Discord Developer Documentation](https://discordapp.com/developers)
for further information.


```
usage: quartermaster [-h] [-V] [-f [CONFIG_FILES [CONFIG_FILES ...]]]
                     [-t TOKEN | -tf [TOKEN_FILE]]
                     [-v {critical,error,warning,info,debug}] [-l [LOG_FILE]]
                     [-lm {w,a}] [-lv {critical,error,warning,info,debug}]

The "Solitude Of War" Discord Bot

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Print version of program
  -f [CONFIG_FILES [CONFIG_FILES ...]], --config-files [CONFIG_FILES [CONFIG_FILES ...]]
                        Configuration file(s) containing command line
                        arguments in JSON format; e.g.,'
                            {
                                "token_file": "quartermaster.key",
                                "verbosity": "warning",
                                "log_file": "quartermaster.log"
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
  -lm {w,a}, --log-file-mode {w,a}
                        Set mode for log file, (over)write, or append.
                        (default: a)
  -lv {critical,error,warning,info,debug}, --log-file-verbosity {critical,error,warning,info,debug}
                        Set log file verbosity. (default: debug)
```
