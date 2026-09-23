"""
UPI Traffic Generator
Sends continuous UPI payment and settlement requests to simulate production traffic.
"""
import time
import random
import requests
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

TXN_SERVICE = os.environ.get('TXN_SERVICE_URL', 'http://upi-transaction-service:8081')
STL_SERVICE = os.environ.get('STL_SERVICE_URL', 'http://upi-settlement-service:8082')
REQUESTS_PER_SECOND = float(os.environ.get('RPS', '2'))

PAYER_VPAS = [
    'rahul@okaxis', 'priya@okicici', 'amit@oksbi', 'meera@okhdfcbank',
    'vijay@ybl', 'sanjay@paytm', 'deepa@upi', 'arjun@ibl',
    'kavita@axl', 'ravi@okaxis', 'neha@oksbi', 'suresh@ybl',
]

PAYEE_VPAS = [
    'swiggy@hdfcbank', 'zomato@icici', 'flipkart@axisbank', 'amazon@sbi',
    'bigbasket@ybl', 'irctc@upi', 'bharatpe@icici', 'phonepe@ybl',
    'gpay@okicici', 'paytm@paytm', 'uber@axisbank', 'ola@hdfcbank',
]

REMARKS = [
    'Food delivery payment', 'Online shopping', 'Train ticket booking',
    'Grocery order', 'Cab fare', 'Electricity bill', 'Mobile recharge',
    'Rent payment', 'Insurance premium', 'Mutual fund SIP',
]


def send_upi_payment():
    """Send a UPI payment request."""
    payload = {
        'payerVpa': random.choice(PAYER_VPAS),
        'payeeVpa': random.choice(PAYEE_VPAS),
        'amount': round(random.uniform(10, 25000), 2),
        'remarks': random.choice(REMARKS),
    }
    try:
        resp = requests.post(f'{TXN_SERVICE}/api/upi/pay', json=payload, timeout=20)
        status = resp.json().get('status', 'UNKNOWN')
        logger.info(f"PAY  | {payload['payerVpa']} -> {payload['payeeVpa']} | INR {payload['amount']:>10.2f} | {status} | HTTP {resp.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"PAY  | FAILED | {e}")


def send_settlement():
    """Send a settlement request."""
    payload = {
        'payerVpa': random.choice(PAYER_VPAS),
        'payeeVpa': random.choice(PAYEE_VPAS),
        'amount': round(random.uniform(100, 50000), 2),
        'remarks': 'Batch settlement',
        'settlementCycle': random.choice(['IMMEDIATE', 'HOURLY', 'EOD']),
    }
    try:
        resp = requests.post(f'{STL_SERVICE}/api/settlement/process', json=payload, timeout=20)
        status = resp.json().get('status', 'UNKNOWN')
        logger.info(f"STL  | {payload['payerVpa']} -> {payload['payeeVpa']} | INR {payload['amount']:>10.2f} | {status} | HTTP {resp.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"STL  | FAILED | {e}")


def main():
    logger.info(f"UPI Traffic Generator started | RPS={REQUESTS_PER_SECOND}")
    logger.info(f"  Transaction Service: {TXN_SERVICE}")
    logger.info(f"  Settlement Service:  {STL_SERVICE}")

    # Wait for services to be ready
    logger.info("Waiting 30s for services to start...")
    time.sleep(30)

    interval = 1.0 / REQUESTS_PER_SECOND
    while True:
        # 70% payments, 30% settlements
        if random.random() < 0.7:
            send_upi_payment()
        else:
            send_settlement()
        time.sleep(interval + random.uniform(-0.1, 0.1))


if __name__ == '__main__':
    main()
