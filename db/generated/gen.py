import datetime
from werkzeug.security import generate_password_hash
import csv
from faker import Faker

num_users = 100
num_products = 2000
num_purchases = 2500
num_feedbacks = 2500

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


# def gen_users(num_users):
#     with open('Users.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Users...', end=' ', flush=True)
#         for uid in range(num_users):
#             if uid % 10 == 0:
#                 print(f'{uid}', end=' ', flush=True)
#             profile = fake.profile()
#             email = profile['mail']
#             plain_password = f'pass{uid}'
#             password = generate_password_hash(plain_password)
#             name_components = profile['name'].split(' ')
#             firstname = name_components[0]
#             lastname = name_components[-1]
#             address = fake.address()
#             balance = f'{str(fake.random_int(max=1000))}'
#             writer.writerow([uid, email, password, firstname, lastname, address, balance])
#         print(f'{num_users} generated')
#     return


# def gen_products(num_products):
#     available_pids = []
#     with open('Products.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Products...', end=' ', flush=True)
#         for pid in range(num_products):
#             if pid % 100 == 0:
#                 print(f'{pid}', end=' ', flush=True)
#             name = fake.sentence(nb_words=4)[:-1]
#             price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
#             available = fake.random_element(elements=('true', 'false'))
#             if available == 'true':
#                 available_pids.append(pid)
#             writer.writerow([pid, name, price, available])
#         print(f'{num_products} generated; {len(available_pids)} available')
#     return available_pids


# def gen_purchases(num_purchases, available_pids):
#     with open('Purchases.csv', 'w') as f:
#         writer = get_csv_writer(f)
#         print('Purchases...', end=' ', flush=True)
#         for id in range(num_purchases):
#             if id % 100 == 0:
#                 print(f'{id}', end=' ', flush=True)
#             uid = fake.random_int(min=0, max=num_users-1)
#             pid = fake.random_element(elements=available_pids)
#             time_purchased = fake.date_time()
#             writer.writerow([id, uid, pid, time_purchased])
#         print(f'{num_purchases} generated')
#     return

def gen_feedbacks(num_feedbacks, num_products=62323):
    with open('Purchases.csv', 'r') as f:
        purchases = list(csv.reader(f))
    
    feedback_combinations = set()  # keep track of existing user-product feedback combos
    feedbacks_written = 0
    
    with open('Feedbacks.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Feedbacks...', end=' ', flush=True)
        
        while feedbacks_written < num_feedbacks:
            purchase = fake.random_element(elements=purchases)
            uid = purchase[1]  
            pid = fake.random_int(min=1, max=num_products)  # simulate product ID within range for now, use Amazon later

            # i want to make sure unique review per product per user
            if (uid, pid) in feedback_combinations:
                continue  # skip if review already exists
            
            feedback_combinations.add((uid, pid))
            feedback_id = feedbacks_written
            comment = fake.sentence()
            rating = fake.random_int(min=1, max=5)
            purchase_time = datetime.datetime.strptime(purchase[3], '%Y-%m-%d %H:%M:%S') 
            feedback_time = purchase_time + datetime.timedelta(days=fake.random_int(min=1, max=30))

            
            writer.writerow([feedback_id, uid, pid, comment, rating, feedback_time.strftime('%Y-%m-%d %H:%M:%S')])
            feedbacks_written += 1
            if feedbacks_written % 100 == 0:
                print(f'{feedbacks_written}', end=' ', flush=True)
        
        print(f'{feedbacks_written} generated.')


# gen_users(num_users)
# available_pids = gen_products(num_products)
# gen_purchases(num_purchases, available_pids)
gen_feedbacks(num_feedbacks)