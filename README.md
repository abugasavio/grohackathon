Gro Hackathon on 5 March
====

Harvesting data from http://www.nass.usda.gov and saving the data in a postgres database.
Running some analysis and saving the analysis in the database.

Usage
---
1. Create a virtual environment.

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

5. Check out [https://github.com/savioabuga/grohackathon/blob/master/harvest.ipynb] for some analysis

Future Features/ Optimization
---
1. Writing tests

2. No need to download if the version of the file in the server is the same as the local one.

3. Optimizing the reading the reading of data into the pandas dataframe

   + [http://stackoverflow.com/questions/14262433/large-data-work-flows-using-pandas](Solution on stackoverflow)
   
   + [http://stackoverflow.com/questions/24251219/pandas-read-csv-low-memory-and-dtype-options](Solution on stackoverflow)


   