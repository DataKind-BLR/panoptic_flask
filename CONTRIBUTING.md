# Steup Instructions

## Credential File Locations

File locations for the following files

* `credentials.yaml`         - should be present in the root directory
* `iff_gsheets_config.json`  - should be present inside the `iff_dashboard` folder

You can change the following values in the `credentials.yaml` file

* `MYSQL_USERNAME`
* `MYSQL_PASSWORD`
* `MYSQL_DATABASE`

## Database Setup

Database name is `panoptic` & the credentials are as per your local system

```bash
mysql -u root -p panoptic < sql_dump.sql
```

## NPM Dependencies

Install the node module dependencies inside the `static` folder

```bash
cd static
npm install
```

## Python Requirements

Run the following command from the root folder

```bash
pip -r requirements.txt
```

## Run

Run the following command from the root directory on the terminal / cmd

```bash
python panoptic_flask.py
```

Open [127.0.0.1:5000](127.0.0.1:5000) in the browser