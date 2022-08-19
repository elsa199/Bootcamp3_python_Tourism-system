from data.points import cities, distances
from packages.tools.common import inp
from packages.utils.env import main as initialize
print('---------------------------------------------------------------------')
print('                     Wellcome to our program                         ')
print('         When ever you wanted to cancel use-> Ctrl + c + Enter       ')
print('---------------------------------------------------------------------\n')


inputs = initialize()




if inputs['type'] == 'customer':
    from packages.routes.customer import main as customer_route, login
    inputs = login(inputs)
    customer_route(cities, distances, ['travel'])
