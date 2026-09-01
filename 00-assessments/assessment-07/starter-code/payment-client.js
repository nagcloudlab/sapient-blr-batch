const axios = require('axios');

const PAYMENT_SERVICE_URL = 'http://localhost:4000';

/**
 * Charge a booking via the payment microservice.
 * @param {string} bookingId - ID of the booking to charge
 * @param {number} amount    - Amount in pence / cents
 * @param {string} method    - Payment method: 'card' | 'upi' | 'wallet'
 * @returns {Promise<object>} Payment confirmation object
 */
async function chargeBooking(bookingId, amount, method) {
  const response = await axios.post(`${PAYMENT_SERVICE_URL}/charge`, {
    bookingId,
    amount,
    method
  });

  return response.data;
}

/**
 * Refund a previously charged booking.
 * @param {string} paymentId - ID of the payment to refund
 * @returns {Promise<object>} Refund confirmation object
 */
async function refundPayment(paymentId) {
  const response = await axios.post(`${PAYMENT_SERVICE_URL}/refund`, {
    paymentId
  });

  return response.data;
}

module.exports = { chargeBooking, refundPayment };
