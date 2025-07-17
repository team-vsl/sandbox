
# VP Bank Hackathon - Challenge 23 Solution

Source code for Challenge 23 solution.

## Collaborators

To be updated later...

## Requirements

During development, the following conditions are required:

1. Development environment: Linux.
2. AWS CLI must be installed.
3. Python (>3.1x) must be installed.

## How to set up?

Instructions for setting things up:

### AWS CLI

1. Log in to the IAM User provided and create an Access Key and Secret Key.
2. Then, configure the AWS CLI profile (make sure AWS CLI is installed).

```bash
aws configure --profile vsl
```

Then enter the Access Key ID, Secret Access Key, Region = `ap-southeast-1`, and Output = `json`.

### Setup environment file

1. In the project directory, create a `.env` file.
2. Copy all contents from `.env.example` to `.env`.
3. Fill in the missing information.

Or run this command to do it quickly:

```bash
cat .env.example > .env
```

### Create DataContract Temporary Directory

1. In the user's home, create the following directory:

```bash
sudo mkdir -p /var/vpbank/datacontracts
```

2. Then give full permissions to this folder:

```bash
sudo chmod -R 777 /var/vpbank/datacontracts
```

### Project

1. First, install Python 3 and pip3 (version >= 3).
2. Install the `python3-venv` library.
3. Create a virtual environment for the project:

```bash
python3 -m venv venv
```

4. Install required packages:

```bash
pip install -r requirements.txt
```

5. Done.

---
