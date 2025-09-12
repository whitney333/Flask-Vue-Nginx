import os
from dotenv import load_dotenv
from mongoengine import connect, disconnect
import pathlib
from sshtunnel import SSHTunnelForwarder


# Global variables for shared state
ssh_tunnel = None
mongo_client = None

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
        print(f"Loaded environment: {environment}")
    else:
        raise FileNotFoundError(f"Environment file '{env_file}' not found.")

    if os.getenv('FLASK_ENV') == 'development':
        try:
            # set up SSH tunneling for dev environment
            ssh_tunnel = SSHTunnelForwarder(
                (os.getenv(key='EC2_URL'), 22),
                ssh_username=os.getenv(key='EC2_USER'),
                ssh_pkey=os.fspath(
                    pathlib.Path(__file__).parent / 'cert' / 'docdb-connect.pem'),
                remote_bind_address=(os.getenv(key='DB_URI'), 27017),
                local_bind_address=('127.0.0.1', 27017)
            )
            # start the tunnel
            ssh_tunnel.start()
            print(f"SSH Tunnel established to {os.getenv(key='DB_URI')}")

            # connect to DocumentDB
            mongo_client = connect(
                host='127.0.0.1',
                port=27017,
                db='general',
                username=os.getenv(key='DB_USER'),
                password=os.getenv(key='DB_PASS'),
                authMechanism="SCRAM-SHA-1",
                tlsAllowInvalidHostnames=True,
                tls=True,
                tlsCAFile=os.fspath(
                    pathlib.Path(__file__).parent / 'cert' / 'global-bundle.pem'),
                timeoutMS=10000,
                retryWrites=False,
                directConnection=True
            )
            print("Successfully connected to DocumentDB")

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
            tlsAllowInvalidHostnames=True,
            tls=True,
            tlsCAFile=os.fspath(
                pathlib.Path(__file__).parent / 'cert' / 'global-bundle.pem'),
            timeoutMS=10000,
            retryWrites=False,
            directConnection=True
        )

def connect_db():
    # Connect to DocumentDB
    mongo_client = connect(
        host =  "mongodb://43.198.77.59:27017/",
        port = 27017,
        db = "general",
        username = os.getenv(key='DB_USER'),
        password = os.getenv(key='DB_PASS')
    )

    return mongo_client
