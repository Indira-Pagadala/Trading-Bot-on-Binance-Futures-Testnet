## Trading Bot (Binance USDT-M Futures Testnet)

### What this project does
- **Simple trading CLI** for placing USDT-M futures orders on **Binance Testnet** (`BTCUSDT` etc.).
- Supports **MARKET**, **LIMIT**, and **STOP‑LIMIT** orders.
- Handles Binance **timestamp drift** automatically and validates **STOP‑LIMIT** orders so they don’t trigger immediately.

### Project structure (files explained)
- **`cli.py`**: Typer-based command-line interface. Shows prompts in the terminal, collects order details, and calls the order logic.
- **`bot/client.py`**: Wraps `python-binance`:
  - Creates a Futures testnet client using API key/secret from environment variables.
  - Syncs a timestamp offset with Binance server time to avoid `-1021` errors.
  - Sends orders via `futures_create_order` and logs requests/responses.
- **`bot/orders.py`**: Builds the final order parameters for Binance (symbol, side, type, prices, time-in-force) and calls `client.place_order`.
- **`bot/validators.py`**: Validates user input:
  - Quantity > 0.
  - MARKET orders have no prices.
  - LIMIT and STOP‑LIMIT require correct price fields.
  - STOP‑LIMIT prices are checked against current mark price to avoid “Order would immediately trigger”.
- **`bot/logging_config.py`**: Central logging setup (formats, levels, handlers, log file path).
- **`logs/trading_bot.log`**: Log file where runs, errors, and Binance responses are written.
- **`.env`**: Holds sensitive config like `BINANCE_API_KEY` and `BINANCE_API_SECRET` (not committed).
- **`requirements.txt`**: Python dependencies for this project.

### Setup steps
1. **Python and virtual environment**
   - Use Python 3.11+ (recommended).
   - From the project root (`Trading_Bot`):
     ```bash
     python -m venv venv
     venv\Scripts\activate  # On Windows
     ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Create and fill `.env`**
   - In the project root, create a file named `.env`:
     ```env
     BINANCE_API_KEY=your_testnet_api_key_here
     BINANCE_API_SECRET=your_testnet_api_secret_here
     ```
   - Keys must be **Binance Futures Testnet** keys, not mainnet.

4. **Confirm Windows time is synced**
   - Go to **Settings → Time & Language → Date & Time → Sync now**.
   - This keeps your system clock close to Binance’s server time. The client also applies an internal offset, but having roughly correct OS time helps.

### How to run it (with examples)
1. **Activate the virtualenv (if not already)**
   ```bash
   venv\Scripts\activate
   ```

2. **Run the interactive trading CLI**
   ```bash
   python cli.py trade
   ```

3. **Example flows**
   - **MARKET BUY BTCUSDT**:
     - Symbol: `BTCUSDT`
     - Side: `BUY`
     - Order type: choose `1` (MARKET)
     - Quantity: e.g. `0.001`

   - **LIMIT SELL BTCUSDT**:
     - Symbol: `BTCUSDT`
     - Side: `SELL`
     - Order type: choose `2` (LIMIT)
     - Quantity: e.g. `0.001`
     - Limit price: e.g. `52000`

   - **STOP‑LIMIT BUY BTCUSDT** (entry above current price):
     - Symbol: `BTCUSDT`
     - Side: `BUY`
     - Order type: choose `3` (STOP‑LIMIT)
     - Quantity: e.g. `0.001`
     - Stop price: **must be ABOVE current mark price**, e.g. if mark is `51000`, pick `51500`.
     - Limit price: a reasonable fill price near the stop, e.g. `51520`.

   On success, the CLI prints the order payload returned by Binance. On failures, it prints clear validation or API error messages and details are logged to `logs/trading_bot.log`.

### Assumptions and things to keep in mind
- **Testnet only**: The client is hardcoded to Binance **USDT‑M Futures Testnet** (`https://demo-fapi.binance.com/fapi`). For real trading you would need to change the base URL and keys carefully.
- **No risk management**: This is a **minimal example bot**, not a full trading system. There is no PnL tracking, position sizing logic, or risk controls beyond basic validation.
- **Network and API limits**:
  - Requests can fail due to network issues or rate limits. Errors are surfaced in the CLI and logs.
  - The client uses a reasonable timeout and `recvWindow` to balance reliability and safety.
- **STOP‑LIMIT behavior**:
  - BUY: stop price must be **above** current mark price.
  - SELL: stop price must be **below** current mark price.
  - The validator enforces this and raises a clear error instead of letting Binance return `-2021`.
- **Logging**: All important events (orders, errors, server time sync, mark prices) are written to `logs/trading_bot.log`. This is the first place to check if something looks off.
