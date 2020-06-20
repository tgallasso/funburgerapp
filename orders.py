import googlemaps, re
import db_connect

gmaps = googlemaps.Client(key='')

# Taking the customer's name
def take_name(user_name = input('Hello, what\'s the customer\'s name? ')):
    while user_name.lower().isdigit():
        user_name = input('Was that the name? We accept only letters. Try it again, please: ')
    return user_name.capitalize()

def take_zip(destination = input('Type the destination\'s zipcode: ')):
    # While the zipcode is not a valid zipcode on the Google Maps API, it keeps asking the zipcode again.
    valid_zipcode = False
    while valid_zipcode != True:
        my_dist = gmaps.distance_matrix('13208080', destination)
        try:
            # Try to get the km on the API
            km = my_dist['rows'][0]['elements'][0]['distance']['text']
        except KeyError:
            print("\nZipcode not valid. Try again.")
            destination = input('Type another destination\'s zipcode or look at it on Google: ')
        else:
            valid_zipcode = True
            return destination

# Getting the distance in km, between the burger place and the customer's house
def km_calculator(destination_in_km = take_zip()):
    # While the zipcode is not a valid zipcode on the Google Maps API, it keeps asking the zipcode again.
    valid_zipcode = False
    while valid_zipcode != True:
        my_dist = gmaps.distance_matrix('13208080', destination_in_km)
        try:
            # Try to get the km on the API
            km = my_dist['rows'][0]['elements'][0]['distance']['text']
        except KeyError:
            print("\nZipcode not valid. Try again.")
            destination_in_km = input('Type another destination\'s zipcode or look at it on Google: ')
        else:
            # If succeeded, use the regular expression to separate the number of km and save it a variable
            km_regex = re.compile(r'\d+(.\d)?')
            km_number = km_regex.search(km)
            valid_zipcode = True
            return round(float(km_number.group()))


#Burgers dictionary
burgers = {'salad': {'Fun Salad': 7.90}, 'bbq': {'Fun Barbecue Bacon': 8.90}, 
            'cheddar': {'Fun Cheddar Bacon': 10.90}, 'egg': {'Fun Egg Bacon': 9.90}, 
            'coca': {'Coca-Cola': 4}, 'guarana': {'Guaraná': 3}, 'adc': {'Adicional': 1.50}}


first_key = []
first_value = []

#Taking orders
def calc_order(order = input('Type the sandwich, soda, add-on or \'exit\' to finish: ')):
    while order.lower() != 'exit':
        while order not in burgers:
            if order != 'exit':
                print(f'\n{order} is not a valid item.')
                order = input('Type another sandwich, soda, add-on or \'exit\' to finish: ')
            if order == 'exit':
                km = km_calculator()    
                zipcode = take_zip()
                first_name = take_name()
                db_connect.add(first_name, str(first_key), (sum(first_value) + km), zipcode)
                return f'\nIt\'s done!\n{first_name}\'s order is ready to cook!\nThe order is: {first_key} making it R$ {round(sum(first_value), 2)} on food items + R$ {km} of delivery tax.\nOn a total of: R$ {round(sum(first_value) + km, 2)}\n'    
        for nickname, name_price in burgers.items():
            if order == nickname:
                for name, price in name_price.items():
                    first_key.append(name)
                    first_value.append(price)
                    order = input('Great. Type another sandwich, soda, add-on or \'exit\' to finish: ')        
    km = km_calculator()
    zipcode = take_zip()
    first_name = take_name()
    db_connect.add(first_name, str(first_key), (sum(first_value) + km), zipcode)
    return f'\nIt\'s done!\n{first_name}\'s order is ready to cook!\nThe order is: {first_key} making it R$ {round(sum(first_value), 2)} on food items + R$ {km} of delivery tax.\nOn a total of: R$ {round(sum(first_value) + km, 2)}\n'      
print(calc_order())




        
        
        
        
        
    
