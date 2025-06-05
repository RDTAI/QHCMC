# Project Name

This project applies human-centered Q-Learning to surgical scheduling within a medical consortium, aiming to optimize resource allocation and improve efficiency while considering healthcare personnel well-being.

## Installation

You can either directly utilize our dataset located in the `dataset` folder. The data format is exemplified as follows:
```csv
| Patient ID | Day      | Start Time | End Time | Duration (hours) | Surgery Type                        | Emergency |
|--------------|----------|--------------|----------|------------------|-------------------------------------|-----------|
| 1            | Sunday   | 13:00        | 15:00    | 2                | Obstetrics and Gynecology Surgery   | No        |
| 2            | Monday   | 12:00        | 13:00    | 1                | Ophthalmic Surgery                  | No        |
| 3            | Friday   | 15:00        | 17:00    | 2                | Gastrointestinal Surgery            | No        |
| 4            | Sunday   | 14:00        | 15:00    | 1                | Obstetrics and Gynecology Surgery   | No        |
```
Alternatively, you can generate synthetic datasets using the script in ` dataset/generate_data.py`:
```bash
python dataset/generate_data.py
```
## Usage
To run the program, clone the repository and execute the main script:
```bash
git clone https://github.com/RDTAI/QHCMC.git
cd QHCMC
python main.py

```
  