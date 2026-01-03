# ⚡ directa-scraper

Fetch zero fees ETF and PAC entries from `directa.it`
Outputs JSONs and CSVs.

## 🚀 Quick Start

Follow these steps to get the `directa-scraper` up and running on your local machine.

### Prerequisites
-   **Python 3.x**: Ensure you have Python 3 installed. You can download it from [python.org](https://www.python.org/downloads/).

### Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/mastershadow/directa-scraper.git
    cd directa-scraper
    ```

2.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

### Usage

To run the scraper, execute the `main.py` script. The script's internal logic will determine the target URLs and data extraction rules.

```bash
python main.py
```

After execution, scraped data will typically be saved in the `out/` directory. You might need to inspect `main.py` to understand specific command-line arguments if supported, or to modify target URLs and extraction logic directly.

## 📁 Project Structure

```
directa-scraper/
├── .idea/                 # IDE configuration files
├── data/                  # Placeholder for input/temporary data
├── main.py                # Main scraping script
├── out/                   # Directory for scraped output data
└── requirements.txt       # Project dependencies
```

## ⚙️ Configuration

The primary configuration for `directa-scraper`, such as target URLs, specific selectors for data extraction, and output formats, is handled directly within the `main.py` script.

### Environment Variables
No explicit environment variables are currently used or required for this script.

### Configuration Files
-   `requirements.txt`: Manages Python package dependencies.
---

<div align="center">

**⭐ Star this repo if you find it helpful!**

Made with ❤️ by [mastershadow](https://github.com/mastershadow)

</div>