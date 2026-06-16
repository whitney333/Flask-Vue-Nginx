import os
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from pathlib import Path
from sshtunnel import SSHTunnelForwarder
import logging

logger = logging.getLogger(__name__)


# Global variables for shared state
# ssh_tunnel = None
# mongo_client = None

BASE_DIR = Path(__file__).resolve().parent

def _require_env(name):
    value = os.getenv(name)
    if value is None or not value.strip():
        raise ValueError(f"env {name} is required for MongoDB connection.")
    return value.strip().strip('"').strip("'")

def connect_docdb():
    # Dynamically load .env.dev or .env.prod
    environment = os.getenv("FLASK_ENV", "development")  # default to 'dev'
    env_file = f".env.{environment}"
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        test = {
            "FLASK_ENV": os.getenv(key="FLASK_ENV"),
            "DB_USER": os.getenv(key="DB_USER"),
            "DB_PASS": os.getenv(key="DB_PASS"),
            "DB_URI": os.getenv(key="DB_URI"),
            "EC2_URL": os.getenv(key="EC2_URL"),
            "EC2_USER": os.getenv(key="EC2_USER")
        }
        # print(test)
        logger.info(f"Loaded environment: {environment}")
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")

    if os.getenv('FLASK_ENV') == 'development':
        try:
            # set up SSH tunneling for dev environment
            ssh_tunnel = SSHTunnelForwarder(
                (os.getenv(key='EC2_URL'), 22),
                ssh_username=os.getenv(key='EC2_USER'),
                ssh_pkey=os.fspath(
                    Path(__file__).parent / 'cert' / 'docdb-connect.pem'),
                remote_bind_address=(os.getenv(key='DB_URI'), 27017),
                local_bind_address=('127.0.0.1', 27017)
            )
            # start the tunnel
            ssh_tunnel.start()
            logger.info(f"SSH Tunnel established to {os.getenv(key='DB_URI')}")

            # connect to DocumentDB
            mongo_client = connect(
                host='127.0.0.1',
                port=27017,
                db='general',
                username=os.getenv(key='DB_USER'),
                password=os.getenv(key='DB_PASS'),
                authMechanism="SCRAM-SHA-1",
                tlsAllowInvalidHostnames=False,
                tls=True,
                tlsCAFile=os.fspath(
                    Path(__file__).parent / 'cert' / 'global-bundle.pem'),
                timeoutMS=10000,
                retryWrites=False,
                directConnection=True
            )
            logger.info("Successfully connected to DocumentDB")

            return mongo_client
        except Exception as e:
            disconnect()
            raise Exception(f"Failed to connect to DocumentDB: {str(e)}")
    else:
        # Connect to DocumentDB
        connect(
            host=os.getenv(key='DB_URI'),
            port=27017,
            db='general',
            username=os.getenv(key='DB_USER'),
            password=os.getenv(key='DB_PASS'),
            authMechanism="SCRAM-SHA-1",
            tlsAllowInvalidHostnames=False,
            tls=True,
            tlsCAFile=os.fspath(
                Path(__file__).parent / 'cert' / 'global-bundle.pem'),
            timeoutMS=10000,
            retryWrites=False,
            directConnection=True
        )


def connect_db():
    global mongo_client

    # load .env file based on environment variable
    environment = os.getenv("FLASK_ENV", "development").strip() or "development"
    env_file = BASE_DIR / f".env.{environment}"

    if env_file.exists():
        # override=False: if the environment variable is already set, it will use env in docker
        load_dotenv(dotenv_path=env_file, override=False)
        logger.info("Loaded environment file: %s", env_file.name)
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")

    # disconnect from any existing connections
    disconnect()

    db_uri = _require_env("DB_URI")
    db_user = _require_env("DB_USER")
    db_pass = _require_env("DB_PASS")
    db_name = os.getenv("DB_NAME", "general").strip()

    auth_source = os.getenv("DB_AUTH_SOURCE", "admin").strip()
    auth_mechanism = os.getenv("DB_AUTH_MECHANISM", "SCRAM-SHA-256").strip()

    try:
        logger.info("Connecting to MongoDB/DocumentDB at %s...", db_uri)

        # connect to MongoDB
        mongo_client = connect(
            db=db_name,
            host=db_uri,  # in local_docker env: "ssh-tunnel:27017"
            username=db_user,
            password=db_pass,
            authentication_source=auth_source,
            authentication_mechanism=auth_mechanism,
            serverSelectionTimeoutMS=10000,
            connectTimeoutMS=10000,
        )
        logger.info("MongoDB connected successfully: db=%s", db_name)
        return mongo_client

    except Exception:
        disconnect()
        logger.exception("Failed to connect to MongoDB.")
        raise
