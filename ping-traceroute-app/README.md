# Ping and Traceroute Application

This project is a Python application that allows users to perform network diagnostics using the ping and traceroute commands. The application provides a user-friendly interface for inputting an address and displaying the results.

## Project Structure

```
ping-traceroute-app
├── src
│   ├── main.py        # Entry point of the application
│   ├── ui.py          # User interface logic
│   └── network.py     # Network functionalities (ping and traceroute)
├── requirements.txt    # Dependencies for the project
└── README.md           # Documentation for the project
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ping-traceroute-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Once the application is running, you can input an address in the provided field and click the buttons to perform ping or traceroute operations. The results will be displayed in the designated area below the buttons.

## Dependencies

Make sure to check the `requirements.txt` file for the list of required libraries.