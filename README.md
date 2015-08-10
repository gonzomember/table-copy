# Table copy

Simple utility script to copy database tables. Works with MySQL.

#### Instalation and usage

To install the script run:
```sh
$ pip install git+https://github.com/gonzomember/table-copy.git#egg=table_copy
```
it is however strongly encouraged to do so inside a `virtualenv`.

To run it, just type:
```sh
$ table-copy --source <source-host> <source-user> <source-pass> <source-db> --target <target-host> <target-user> <target-pass> <source-db>
```

#### Setting up for development

Clone the repo with `git clone https://github.com/gonzomember/table-copy.git` and that's it. To run tests `cd` into the repo root directory and type `python setup.py test`
