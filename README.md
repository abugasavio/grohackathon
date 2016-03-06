Gro Hackathon on 5 March
====

Harvesting data from http://www.nass.usda.gov and saving the data in a postgres database.
Running some analysis and saving the analysis in the database.

Usage
---
1. Create a virtualenv.
2. Clone the package and install it in the virtual environment
    ```
    git clone https://github.com/savioabuga/grohackathon.git
    ```
3. Install the requirement
    ```
    pip install -r requirements.txt
    ```
4. Then use the package
    ```
    python harvest.py
    ```
   With the following options
   ­­start_date​=%Y­%m­%d
   ­­end_date​=%Y­%m­%d
   ­­database_name​=
   ­­database_host​=
   ­­database_user​=
   ­­database_pass​=

