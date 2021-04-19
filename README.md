# More StatCan!

The Canadian government has a statistics agency aptly named "Statistics Canada" ("StatCan" for short).  Their data is in the form of data cubes, and available for public RESTful consumption. 

This project pulls a few slices from those cubes.


## Execution

This program is very simple; it is more useful for understanding how the phrase the data extraction calls rather than for the data pulled.

Windows
```
git clone https://github.com/klahnakoski/mo-statcan.git
cd mo-statcan
pip install -r requirements.txt
set PYTHONPATH=.;vendor
python pull_data.py
```




## References

* reference docs - https://www.statcan.gc.ca/eng/developers/wds
* dev user guide - https://www.statcan.gc.ca/eng/developers/csv/user-guide
* Delta files - https://www.statcan.gc.ca/eng/developers/df

