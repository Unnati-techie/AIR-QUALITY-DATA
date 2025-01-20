# Air Quality Data (India)

This project provides a RESTful API to collect, store, and manage air quality data for cities in India. It uses data fetched from the [OpenAQ API](https://openaq.org/) and stores the data in a PostgreSQL database. The application is built using Flask and SQLAlchemy, with asynchronous data fetching using `aiohttp` to efficiently handle large datasets. The collected data can be accessed and queried through a web interface.

## Features

- **Real-Time Data Fetching**: Fetch air quality measurements (such as PM2.5, PM10, CO, NO2, etc.) from the OpenAQ API in real-time.
- **Structured Data Storage**: Store structured data using PostgreSQL, with relationships between cities, countries, and air quality measurements.
- **Web Interface**: A user-friendly interface to view the air quality data in tabular format.
- **Scheduled Data Updates**: Automatically fetch and update data every day at midnight using Python's `schedule` library.
- **Cross-Origin Resource Sharing (CORS)**: Ensures the application can be accessed by clients from different domains.

## Technologies Used

- **Flask**: Web framework for creating the API and handling HTTP requests.
- **SQLAlchemy**: ORM for interacting with the PostgreSQL database.
- **PostgreSQL**: A powerful, open-source relational database used for storing the data.
- **aiohttp**: Asynchronous HTTP client for making API requests.
- **dotenv**: To manage environment variables (e.g., API keys, database URL).
- **schedule**: Python library for scheduling periodic tasks.
- **HTML/CSS**: Frontend technologies for displaying data in a clean and responsive format.

## Getting Started

### Prerequisites

1. **Python 3.7+**: Ensure Python is installed on your machine.
2. **PostgreSQL**: You need a PostgreSQL database for storing the air quality data.
3. **Environment Variables**: Use a `.env` file to store sensitive credentials (e.g., API keys, database URLs).

### Setup Instructions

Follow these steps to set up the project:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Unnati-techie/AIR-QUALITY-DATA.git
   cd AIR-QUALITY-DATA
   
2. **Create and activate a virtual environment**:
   
   **For macOS/Linux**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. **Install the required dependencies**:
   
   ```bash
   pip install -r requirements.txt

4. **Set up environment variables**:
   
 ```env
   DATABASE_URL=your_postgresql_database_url
   API_KEY=your_openaq_api_key


  
