# scheduler.py
import re
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from bnb_interaction import send_transaction

# Initialize and start the background scheduler.
scheduler = BackgroundScheduler()
scheduler.start()

def execute_payment(payment_details: dict):
    """Execute a scheduled payment using the blockchain interaction helper."""
    address = payment_details.get("address")
    amount = float(payment_details.get("amount"))
    try:
        tx_hash = send_transaction(address, amount)
        print(f"Scheduled Payment Executed: TX Hash {tx_hash}")
        # You might also update logs or notify the user here.
    except Exception as e:
        print(f"Error executing scheduled payment: {e}")

def schedule_payment(payment_details: dict, scheduled_time: str):
    """
    Schedule a payment. The scheduled_time can be provided as either:
      - A relative time string (e.g., "in 5 minutes" or "in 30 seconds")
      - An absolute ISO-formatted datetime string.
    
    If a relative time is provided, it will be converted to an absolute time.
    In all cases, the resulting run date must be in the future.
    """
    now = datetime.utcnow()
    run_date = None

    # Check if the scheduled_time is relative (e.g., "in 5 minutes", "in 30 seconds")
    if scheduled_time.lower().startswith("in "):
        # Updated regex: allow "minut" or "minute" (optionally with trailing s) as well as seconds/hours.
        pattern = r"in\s+(\d+)\s*(second(?:s)?|minut(?:e)?(?:s)?|hour(?:s)?)"
        match = re.search(pattern, scheduled_time.lower())
        if match:
            quantity = int(match.group(1))
            unit = match.group(2)
            # Use substring matching so that "minut" or "minute" both trigger minutes.
            if "second" in unit:
                delta = timedelta(seconds=quantity)
            elif "minut" in unit:
                delta = timedelta(minutes=quantity)
            elif "hour" in unit:
                delta = timedelta(hours=quantity)
            else:
                raise ValueError("Unsupported time unit in relative time.")
            run_date = now + delta
        else:
            raise ValueError(f"Could not parse relative time: {scheduled_time}")
    else:
        # Assume the scheduled_time is an absolute ISO datetime string.
        try:
            # Remove any trailing 'Z' if present and parse.
            run_date = datetime.fromisoformat(scheduled_time.rstrip("Z"))
        except Exception as e:
            raise ValueError(f"Invalid scheduled_time format: {scheduled_time}") from e

    # Verify that the computed run_date is in the future.
    if run_date <= now:
        raise ValueError(f"Scheduled time must be in the future. Provided: {run_date.isoformat()}, Current: {now.isoformat()}")

    print(f"Scheduling payment for: {run_date.isoformat()}")
    scheduler.add_job(execute_payment, 'date', run_date=run_date, args=[payment_details])
