# Bacteria Analyzer

## Data flow
Arduino Nano (8 RAW channels, 0-1023)
-> PySerial
-> CSV
-> Python analyzer
-> 2 reference curves + 6 test curves
-> normalization
-> similarity comparison
-> SENSITIVE / RESISTANT / INCONCLUSIVE

Channel order:
1 resistance_reference
2 sensitivity_reference
3-8 test_1 ... test_6

## Run
pip install -r requirements.txt

Test:
python analyzer.py demo_data.csv

Graphs:
python plot_report.py demo_data.csv

GUI:
python app.py

Real Arduino:
python serial_logger.py --port COM9 --baud 9600 --output data.csv

Arduino should send one line containing exactly 8 RAW values, e.g.
523,524,525,512,518,520,517,519

The demo data are synthetic and are NOT real bacterial/clinical measurements.
The algorithm must be validated on real experimental data before scientific or
diagnostic use. The current "SENSITIVE/RESISTANT" result is a software
classification label based on curve similarity, not a medical diagnosis.
