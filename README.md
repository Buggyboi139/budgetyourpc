# BudgetYourPC

## Overview
BudgetYourPC is a dynamic web application engineered to aggregate hardware pricing and automatically provision custom PC builds based on strict user-defined financial brackets. It handles complex data filtering and conditional logic to match compatible components within localized budget constraints.

## Architecture & Data Flow
The application utilizes a decoupled architecture, isolating the backend data ingestion pipeline from the client-side presentation layer.

* **Frontend Client:** A lightweight, client-side interface (`index.html`) that manages state and dynamically renders hardware components based on user input parameters.
* **Data Store:** Hardware inventory and pricing are maintained within a static JSON endpoint (`products.json`).
* **Backend Automation:** A Python-based ingestion pipeline (`update_prices.py`), orchestrated by shell scripting (`run_update.sh`), processes upstream hardware pricing to ensure the data store remains accurate without manual intervention.

## Technology Stack
* **Frontend:** HTML5, CSS3, Vanilla JavaScript
* **Backend/Processing:** Python 3
* **Automation:** Bash / Shell Scripting
* **Data Storage:** JSON

## Threat Model & Security Considerations
This project was structured to analyze how financial constraint algorithms and automated data pipelines can be secured against injection and logic bypasses.

### 1. Parameter Tampering & Input Validation
* **Vector:** Applications calculating budgets and filtering hardware based on user-supplied price brackets are prime targets for parameter tampering. If a user intercepts the request or manipulates the DOM to submit malformed data (e.g., negative integers, excessive string lengths, or unexpected characters), it could induce unhandled exceptions or logic bypasses in the filtering algorithm.
* **Mitigation Strategy:** Strict type-checking and bounds validation must be enforced on all user inputs prior to querying the dataset. In a backend-heavy implementation, these inputs must be parameterized to prevent SQL or NoSQL injection attacks against the hardware database.

### 2. Upstream Data Ingestion (Supply Chain)
* **Vector:** The automated Python pipeline (`update_prices.py`) inherently trusts the external sources it pulls pricing from. If an upstream source is compromised to return malicious payloads within hardware names or descriptions (e.g., `<script>alert(1)</script>`), the pipeline could blindly commit this to `products.json`.
* **Mitigation Strategy:** Implementation of aggressive data sanitization and output encoding within the Python script before writing to the JSON store, neutralizing potential Cross-Site Scripting (XSS) vectors before they reach the client.

### 3. DOM-Based Manipulation
* **Vector:** Because the application dynamically constructs the DOM based on the JSON payload and user selections, improper handling of these variables in JavaScript could lead to DOM-based XSS. 
* **Mitigation Strategy:** Utilizing secure DOM manipulation methods (e.g., assigning text via `textContent` or `innerText` instead of `innerHTML`) when rendering hardware specifications and pricing to the end user.
