import json
import knackpy

"""
Quick start for repl experimentation. Run as: `python -i knack_exp.py`
"""

#
# Sample usage:
#
# $ python -i knack_exp.py
# >>> app.info()
# {'objects': 7, 'scenes': 9, 'records': 5560, 'size': '1.05gb'}
# >>> last5
# [<Record '02/13/2021'>, <Record '02/13/2021'>, <Record '02/13/2021'>, <Record '02/13/2021'>, <Record '02/13/2021'>]
# >>> r
# <Record '02/13/2021'>
#

APP_ID = "5faae3b10442ac00165da195"
API_KEY = "renderer"

app = knackpy.App(app_id=APP_ID, api_key=API_KEY)

last5 = app.get("Covid Events", record_limit=5)

r = last5[0]
