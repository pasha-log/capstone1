from secrets import SECRET_API_KEY
import requests

response = requests.get('https://www.carboninterface.com/api/v1/estimates', params={'key': SECRET_API_KEY, 'location': '471 Belden St.'})