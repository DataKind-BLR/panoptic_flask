# Steup Instructions

## Database Setup

Database name is `panoptic` & the credentials are as per your local system

```bash
mysql -u root -p panoptic < sql_dump.sql
```

Create a `credentials.yaml` file in your root directory with the following structure.

Replace the necessary content in the yaml file, without any quotation.

```yaml
# MySQL
MYSQL_HOST: localhost
MYSQL_USERNAME: <root> 		# Enter DB username
MYSQL_PASSWORD: <root> 		# Enter DB password
MYSQL_DATABASE: <panoptic>  # Enter DB name
MYSQL_PORT: 3306 			# Default MySQL port
```


## NPM Dependencies

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