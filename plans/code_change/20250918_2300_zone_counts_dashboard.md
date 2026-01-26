# Zone Counts Dashboard

## Overview

This is a lightweight dashboard application that fetches and displays data from the `vw_122_zone_counts_by_update_pivoted2` API endpoint. The application provides a user-friendly interface to view zone count data with real-time refresh capabilities.

Based on the sample data, this endpoint provides information about trading zone counts, including buy and sell counts for different price zones (beyondTarget, darkgreen, green, yellow, pink, red, beyondstop) along with timestamps and current price.

## Features

1. **Data Visualization**: Displays zone count data in a clean, tabular format
2. **Real-time Refresh**: Allows users to manually refresh data with the click of a button
3. **Responsive Design**: Works well on both desktop and mobile devices
4. **Error Handling**: Gracefully handles API errors and displays meaningful messages to users
5. **Data Formatting**: Automatically formats timestamps and prices for better readability

## Technical Details

### Architecture

The application is built using:
- **FastAPI**: For the backend API and serving static files
- **HTML/CSS/JavaScript**: For the frontend dashboard
- **Requests**: For making HTTP calls to the data source API

### Project Structure

```
zone_counts_dashboard/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── test_data.py          # Test script with sample data
├── static/
│   ├── style.css          # Stylesheet for the dashboard
│   └── script.js          # Client-side JavaScript
```

### API Endpoints

1. `GET /` - Serves the main dashboard page
2. `GET /api/data` - Returns the zone count data from the source API

### Data Structure

The data includes the following columns:
- `last_update`: Timestamp of the last update
- `beyondTarget_buy/sell`: Count of buy/sell trades beyond target
- `darkgreen_buy/sell`: Count of buy/sell trades in dark green zone
- `green_buy/sell`: Count of buy/sell trades in green zone
- `yellow_buy/sell`: Count of buy/sell trades in yellow zone
- `pink_buy/sell`: Count of buy/sell trades in pink zone
- `red_buy/sell`: Count of buy/sell trades in red zone
- `beyondstop_buy/sell`: Count of buy/sell trades beyond stop
- `current_price`: Current market price
- `captured_on`: Timestamp when the data was captured

### How It Works

1. The application starts a FastAPI server on port 8001
2. When a user visits the root URL, the dashboard HTML is served
3. The frontend JavaScript makes a request to `/api/data` to fetch zone count data
4. The backend fetches data from `http://127.0.0.1:8000/api/vw_122_zone_counts_by_update_pivoted2`
5. The data is processed and returned as JSON to the frontend
6. The frontend displays the data in a formatted table

## Setup and Installation

### Prerequisites

- Python 3.7+
- Pip (Python package installer)

### Installation Steps

1. Navigate to the project directory:
   ```
   cd zone_counts_dashboard
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Start the application:
   ```
   python app.py
   ```

4. Access the dashboard in your browser at:
   ```
   http://127.0.0.1:8001
   ```

## Usage

1. Open your web browser and navigate to `http://127.0.0.1:8001`
2. The dashboard will automatically load the zone count data
3. Click the "Refresh Data" button to manually update the data
4. The table will display all available columns from the data source with formatted values

## Customization

### Styling

To modify the appearance of the dashboard, edit the `static/style.css` file.

### Functionality

To modify the behavior of the dashboard, edit the `static/script.js` file.

### Backend

To modify the backend functionality, edit the `app.py` file.

## Troubleshooting

### Common Issues

1. **"Connection refused" error**: Ensure that the source API at `http://127.0.0.1:8000` is running
2. **Missing dependencies**: Run `pip install -r requirements.txt` to install all required packages
3. **Port conflicts**: Modify the port in `app.py` if 8001 is already in use

### Error Messages

- **"Error Loading Data"**: This indicates a problem connecting to the source API
- **"No data available"**: This means the API returned an empty dataset

## Future Enhancements

1. Add automatic data refresh at regular intervals
2. Implement data filtering and sorting capabilities
3. Add chart visualizations for the zone count data
4. Include authentication and user management
5. Add export functionality for the data (CSV, Excel)
6. Implement pagination for large datasets
7. Add color-coding for different zones in the table

## Dependencies

- fastapi==0.68.0
- uvicorn==0.15.0
- requests==2.26.0
- aiofiles==24.1.0

## License

This project is proprietary and intended for internal use only.