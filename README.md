# JoJo Wiki Scraper 🕵️‍♂️✨

This is a web scraping project built in Python designed to extract detailed character information from the [JoJo's Bizarre Encyclopedia](https://jojowiki.com), the JoJo Wiki.

## 📚 Table of Contents

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Setup & Usage](#️-setup--usage)
- [Example Output](#-example-output)
- [Contributing](#-contributing)


## 📌 Features

✅ Scrapes character names, stand names, abilities, images, and more.  
✅ Supports scraping from character/stand list pages.  
✅ Saves data into JSON, CSV, or a database (extensible).  
✅ Designed with modularity to allow future expansion.  


## 🚀 Tech Stack

- Python 3.x
- `requests`
- `BeautifulSoup4`
- `Selenium` (optional for dynamic content)
- `pandas` (optional for data export)
- `re` (regex for parsing)


## 🧪 Example Output

```json
[
  {
    "name": "Jotaro Kujo",
    "stand": "Star Platinum",
    "abilities": ["Superhuman strength", "Time Stop"],
    "image": "https://jojowiki.com/images/..."
  },
  ...
]
```


## ⚙️ Setup & Usage

### 1. Clone the repository

```bash
git clone https://github.com/chokkoramo/JoJoData.git
```
```bash
cd JoJoData
```

### 2. Install requirements

```bash
pip install -r requirements.txt
```

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
