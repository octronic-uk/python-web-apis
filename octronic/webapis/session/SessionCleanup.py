from octronic.webapis.session.SessionDB import SessionDB
import time
import logging

# Setup Logging
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Create SessionDB
delay = 60
session_db = SessionDB()

# Main
if __name__ == "__main__":
    log.info("Starting SessionDB Cleanup. Running every %d seconds",delay)
    while True:
        log.info("Deleting expired sessions...")
        result = session_db.clear_expired_sessions()
        log.info("Deleted %d sessions.",result.deleted_count)
        time.sleep(delay)

