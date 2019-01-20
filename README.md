# Muboxd
Script to update movies currently on MUBI curated list to a Letterboxd list.

Why? Because I want to sort the list by averaged rating from Letterboxd users. I don't have time to watch every single movie on the list nor reading reviews for every movies. :cry:

My list: https://letterboxd.com/sollicitudin/list/mubi-now-showing-vietnam-region/by/rating/

# Installation
```pip install -r requirements.txt```

# Running
For first time run, edit `credentials.json` file using your account information. We use cookie data for MUBI and account detail for Letterboxd. Also, provide your Letterboxd list link, get the edit link (with /edit/ at the end)

Then run

```python start.py```
