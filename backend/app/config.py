import os

"""
Configuration loaded by all services for deployment options, paths, etc.
"""

# Deployment
app_version = "1.0.0.0000"

# Environment settings (dev|qa|prod)
if os.getenv("PYTHON_SHELL") != "cli":
    app_env = os.getenv("MDOT_ENV")
else:
    app_env = os.getenv("mapi_app_env", "qa")

# Staging settings
if os.getenv("PYTHON_SHELL") != "cli":
    app_stage = os.getenv("MDOT_STAGE")
else:
    app_stage = os.getenv("mapi_app_stage", "qa")

# Log environment and stage if running in CLI
if os.getenv("PYTHON_SHELL") == "cli":
    print(f"$app_stage={app_stage}")
    print(f"$app_env={app_env}")

# Paths
path_root = os.getenv("DOCUMENT_ROOT", "/")
app_server = f"http://{os.getenv('SERVER_NAME', 'localhost')}"
path_base = app_server

path_svc = "/"
path_svc_root = path_root
path_svc_common = os.path.join(path_svc_root, "common")
path_services = os.path.join(path_svc_root, "services")

# Database configuration
db_host = os.getenv("DB_HOST", "s4-postgresql-dev-test.cnq78cujpibv.us-west-2.rds.amazonaws.com")
db_user = os.getenv("DB_USER","postgres")
db_password = os.getenv("DB_PASSWORD","postgres2")
database_name = "leadspam"
s4_database_name = os.getenv("S4_DATABASE_NAME", "leadspam")

# Cache configuration
cache_enabled = False
cache_host = os.getenv("CACHE_HOST")
cache_host_port = os.getenv("CACHE_HOST_PORT", "6379")

# Spam lead time interval thresholds
spam_lead_time_interval_threshold_short = 60
spam_lead_time_interval_threshold_long = 900

# Host configurations
host_lead_capture_service = os.getenv("LEAD_CAPTURE_SERVICE")
hosts_s4_service_list = os.getenv("S4_SERVICE_LIST")