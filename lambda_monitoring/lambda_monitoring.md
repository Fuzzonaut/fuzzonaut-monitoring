# Lambda Uptime Monitor

This Lambda function monitors the availability of a given website (e.g., https://fuzzonaut.me) and sends an email notification when the site is unreachable.

---

## 🔁 Trigger

This function is triggered on a **schedule** (using EventBridge) to check the site every few minutes.

---

## 🔔 Notification

If the website is down, the function publishes a message to the SNS topic:
