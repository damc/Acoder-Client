# Acoder client

https://acoder.herokuapp.com/

Acoder is an application that generates code using AI. It can accomplish small programming tasks. This is only the client part of the application. The actual task solving happens on the server (the application sends a request to the server) and the server construct a prompt (and handles few other things) and sends a request to the OpenAI server in order to solve the task.

## Development environment

If you want to use Acoder client in order to develop it, set the following environment variable:

```
export ACODER_CLIENT_ENV='dev'
```

## Creating executables

In order to generate an executable, you need to have Python3 and PyInstaller installed.

Once it is installed, you can generate the executable for Linux:

```
pyinstaller -n acoder_linux --add-data=client/templates/standard.md:client/templates --clean --onefile bin/main.py
```

For Mac OS, you can use the same command, only with a different name for the generated file:

```
pyinstaller -n acoder_mac_os --add-data=client/templates/standard.md:client/templates --clean --onefile bin/main.py
```

For Windows, you can use the below command (note the difference: `;` instead of `:`):

```
pyinstaller -n acoder_windows.exe --add-data=client/templates/standard.md;client/templates --clean --onefile bin/main.py
```

The executables will be saved in `dist` folder.
