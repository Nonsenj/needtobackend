# Please do as the following, or you might end up with some failures on your cmd lol.

### Firstly created your py env
``` bash python -m venv venv ```

### Then activate your env
``` bash venv\Scripts\actvate ```
Be sure to use the command on your os, For ex this is for window

### Install all the dependecies and package with poetry
``` bash pip install poetry ```
then
``` bash poetry install ```

### initial your db first or else it won't be connected
``` bash python -m scripts.initial-db ```

### Run the app

``` bash scripts\run-api.bat ```
Note: if it won't run pls check that the name of the folder inside is correct as your folder name

### To test use 
``` bash poetry run pytest -v ```
