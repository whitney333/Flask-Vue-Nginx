import os
from dotenv import load_dotenv
from mongoengine import connect, disconnect
import pathlib
from sshtunnel import SSHTunnelForwarder


def connect_db(app):
    # Dynamically load .env.dev or .env.prod
    environment = os.getenv("FLASK_ENV", "development")  # default to 'dev'
    env_file = f".env.{environment}"
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
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
                    pathlib.Path(__file__).parent / 'docdb-connect.pem'),
                remote_bind_address=(os.getenv(key='DB_URI'), 27017),
                local_bind_address=('127.0.0.1', 27017)
            )
            # start the tunnel
            ssh_tunnel.start()
            print(f"SSH Tunnel established to {os.getenv(key='DB_URI')}")

            # connect to DocumentDB
            connect(
                host='127.0.0.1',
                port=27017,
                db='general',
                username=os.getenv(key='DB_USER'),
                password=os.getenv(key='DB_PASS'),
                authMechanism="SCRAM-SHA-1",
                tlsAllowInvalidHostnames=True,
                tls=True,
                tlsCAFile=os.fspath(
                    pathlib.Path(__file__).parent / 'global-bundle.pem'),
                timeoutMS=10000,
                retryWrites=False,
                directConnection=True
            )
            print("Successfully connected to DocumentDB")

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
                pathlib.Path(__file__).parent / 'global-bundle.pem'),
            timeoutMS=10000,
            retryWrites=False,
            directConnection=True
        )
