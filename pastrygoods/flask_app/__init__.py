# __init__.py
from flask import Flask
import re


DATABASE = 'pastrygoods'

app = Flask(__name__)
app.secret_key = "Coding3"