<p align="center">
    <img height="128" src="./OCRP7/static/LITReviews.svg">
</p>

> NOTE : `Python 3.9.6` & `Windows 10 21H1` was used while working on this project.

> NOTE : I already know that `LIT Reviews` already have a logo, but i decided to make my own to experiment.

## Installation

We will need to create a virtual environment

```
python -m venv .venv
```

---

Then activate it

```
[WINDOWS]
python ./.venv/Scripts/activate

[LINUX]
source .venv/bin/activate
```

---

Once done, Install all the required dependencies using pip:

```
pip install -r requirements.txt
```

## Running the Project

Running django :

```
python ./manage.py runserver
```

you should see something like this :

```
System check identified no issues (0 silenced).
November 14, 2021 - 11:30:58
Django version 3.2.5, using settings 'OCRP7.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Then navigate to : http://127.0.0.1:8000/

> NOTE : if this isn't what you are seeing, and you are unable to see the website, its probably because there is a typo somewhere or didn't follow the step correctly ...

## Available Accounts

There is few account available for testing, few posts has been already added for showcase

| Username   | Password          | SuperUser |
| :--------- | :---------------- | :-------- |
| `Benjamin` | `NPHt6z3MdyEm8bz` | `no`      |
| `Gabin`    | `Vixyk6qRNPvWSsW` | `no`      |
| `NjustN`   | `i44cB74hTVhPWD9` | `no`      |

