import os
import logging
from logging.handlers import RotatingFileHandler
import psycopg2
from flask import Flask, jsonify
from db_pg_connect import connect  # Import the connect function from db_pg_connect
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define log directory
LOG_DIR = "./logs"
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
os.makedirs(LOG_DIR, exist_ok=True)  # Create log directory if it doesn't exist

# Configure logging
log_file = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        RotatingFileHandler(log_file, maxBytes=1000000, backupCount=5),  # Rotating logs
        logging.StreamHandler(),  # Log to console as well
    ],
)

logger = logging.getLogger(__name__)


@app.route("/")
def home():
    return "Welcome to the Tenant API! Use /api/tenants to fetch data."


@app.route("/favicon.ico")
def favicon():
    return "", 204  # No Content


@app.route("/api/tenants", methods=["GET"])
def get_tenants():
    logger.info("GET /api/tenants request received")
    conn = None

    try:
        # Establish database connection
        conn = connect()
        if not conn:
            logger.error("Failed to connect to the database")
            return jsonify({"error": "Failed to connect to the database"}), 500

        cur = conn.cursor()
        logger.info("Executing tenant data query")
        query = """
            SELECT
                tenant_name,
                tenant_address,
                admission_fee,
                agreed_rent,
                join_date
            FROM tenant_info
        """
        cur.execute(query)
        tenants = cur.fetchall()
        cur.close()

        logger.info("Tenant data fetched successfully")
        # Format the data as JSON
        return jsonify(
            [
                {
                    "tenant_name": row[0],
                    "tenant_address": row[1],
                    "admission_fee": float(row[2]) if row[2] is not None else 0.0,
                    "agreed_rent": float(row[3]) if row[3] is not None else 0.0,
                    "join_date": row[4].isoformat() if row[4] is not None else None,
                }
                for row in tenants
            ]
        )
    except psycopg2.Error as db_error:
        logger.exception("Database error occurred")
        return jsonify({"error": "Database query failed"}), 500
    except Exception as e:
        logger.exception("Unexpected error occurred")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")


@app.route("/api/tenant/<tenant_name>", methods=["GET"])
def get_tenant_details(tenant_name):
    logger.info(f"GET /api/tenant/{tenant_name} request received")
    conn = None

    try:
        conn = connect()
        if not conn:
            logger.error("Failed to connect to the database")
            return jsonify({"error": "Failed to connect to the database"}), 500

        cur = conn.cursor()
        logger.info(f"Fetching details for tenant: {tenant_name}")
        query = """
            SELECT
                tenant_name,
                tenant_address,
                admission_fee,
                agreed_rent,
                join_date
            FROM tenant_info
            WHERE tenant_name = %s
        """
        cur.execute(query, (tenant_name,))
        tenant = cur.fetchone()
        cur.close()

        if not tenant:
            logger.warning(f"No tenant found with name: {tenant_name}")
            return jsonify({"error": "Tenant not found"}), 404

        logger.info(f"Details fetched for tenant: {tenant_name}")
        return jsonify(
            {
                "tenant_name": tenant[0],
                "tenant_address": tenant[1],
                "admission_fee": float(tenant[2]) if tenant[2] is not None else 0.0,
                "agreed_rent": float(tenant[3]) if tenant[3] is not None else 0.0,
                "join_date": tenant[4].isoformat() if tenant[4] is not None else None,
            }
        )
    except Exception as e:
        logger.exception("Error fetching tenant details")
        return jsonify({"error": str(e)}), 500
    finally:
        if conn:
            conn.close()
            logger.info("Database connection closed")


@app.route("/health", methods=["GET"])
def health_check():
    logger.info("Health check accessed")
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    logger.info("Starting Flask application")
    app.run(debug=True)
