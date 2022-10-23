from secrets import SECRET_API_KEY
import requests

response = requests.get(url='https://www.carboninterface.com/api/v1/vehicle_makes', headers={
    'Authorization': f'Bearer {SECRET_API_KEY}',
    'Content-Type': 'application/json'
})

data = response.json()

def get_all_vehicle_brands():
    VEHICLE_BRAND_NAMES = [] 
    for brand in data: 
        id = brand['data']['id']
        name = brand['data']['attributes']['name']
        VEHICLE_BRAND_NAMES.append((id, name))
    return VEHICLE_BRAND_NAMES

units = {
        "g": "carbon_g",
        "kg": "carbon_kg",
        "lbs": "carbon_lb",
        "mt(metric tonnes)": "carbon_mt"
    }

def get_vehicle_estimate(distance_value, distance_unit, vehicle_model_id, emission_unit):
    url = 'https://www.carboninterface.com/api/v1/estimates'

    headers = {'Authorization': f'Bearer {SECRET_API_KEY}', 'Content-Type': 'application/json'}

    data = {
        'type': 'vehicle',
        "distance_unit": f"{distance_unit}",
        "distance_value": f'{distance_value}',
        "vehicle_model_id": f'{vehicle_model_id}'
    }

    res = requests.post(url, headers=headers, json=data)
    data = res.json()

    for key in units.keys(): 
        if key == emission_unit:
            carbon_unit = units[key] 
            return data['data']['attributes'][f'{carbon_unit}']

def get_shipping_estimate(weight_unit, weight_value, distance_unit, distance_value, transport_method, emission_unit):
    url = 'https://www.carboninterface.com/api/v1/estimates'

    headers = {'Authorization': f'Bearer {SECRET_API_KEY}', 'Content-Type': 'application/json'} 

    data = {
        "type": "shipping",
        "weight_value": f"{weight_value}",
        "weight_unit": f"{weight_unit}",
        "distance_value": f'{distance_value}',
        "distance_unit": f"{distance_unit}",
        "transport_method": f"{transport_method}"
    }

    res = requests.post(url, headers=headers, json=data)
    result = res.json() 

    for key in units.keys(): 
        if key == emission_unit:
            carbon_unit = units[key] 
            return result['data']['attributes'][f'{carbon_unit}']

def get_flight_estimate(distance_unit, distance_value, emission_unit):
    avg_lbs_per_mile = 53
    km_in_mile = 1.6
    kg_in_lb = .45
    g_in_lb = 453.59
    mt_in_lb = .0005
    mi_in_km = 0.621
    if distance_unit == "mi" and emission_unit == 'lbs': 
        return distance_value * avg_lbs_per_mile
    elif distance_unit == 'mi' and emission_unit == 'kg': 
        return distance_value * avg_lbs_per_mile * kg_in_lb
    elif distance_unit == 'mi' and emission_unit == 'g':
        return distance_value * avg_lbs_per_mile * g_in_lb
    elif distance_unit == 'mi' and emission_unit == 'mt(metric tonnes)':
        return distance_value * avg_lbs_per_mile * mt_in_lb
    elif distance_unit == "km" and emission_unit == 'lbs': 
        return distance_value * avg_lbs_per_mile * mi_in_km
    elif distance_unit == 'km' and emission_unit == 'kg': 
        return distance_value * avg_lbs_per_mile * kg_in_lb * mi_in_km
    elif distance_unit == 'km' and emission_unit == 'g':
        return distance_value * avg_lbs_per_mile * g_in_lb * mi_in_km
    else:
        return distance_value * avg_lbs_per_mile * mt_in_lb * mi_in_km
    
def get_electricity_estimate(electricity_value, electricity_unit, country, emission_unit): 
    url = 'https://www.carboninterface.com/api/v1/estimates'

    headers = {'Authorization': f'Bearer {SECRET_API_KEY}', 'Content-Type': 'application/json'} 

    data = {
        "type": "electricity",
        "electricity_unit": f"{electricity_unit}",
        "electricity_value": f"{electricity_value}",
        "country": f"{country}"
    }

    res = requests.post(url, headers=headers, json=data)
    result = res.json() 

    for key in units.keys(): 
        if key == emission_unit:
            carbon_unit = units[key] 
            return result['data']['attributes'][f'{carbon_unit}']


