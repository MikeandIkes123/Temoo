import datetime
from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import pandas as pd 
import random
import math


num_users = 100

num_products = 2000
available_pids = num_products

num_purchases = 2500
num_feedbacks = 2500
num_sellers = 5

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')


def gen_users(num_users):
    with open('Users.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Users...', end=' ', flush=True)
        for uid in range(num_users):
            if uid % 10 == 0:
                print(f'{uid}', end=' ', flush=True)
            profile = fake.profile()
            email = profile['mail']
            plain_password = f'pass{uid}'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = fake.address()
            balance = f'{str(fake.random_int(max=1000))}'
            writer.writerow([uid, email, password, firstname, lastname, address, balance])
        print(f'{num_users} generated')
    return


def gen_products():
    available_pids = []
    prod_df = pd.read_csv('db/generated/Amazon_Products.csv', header=None)
    prod_df.columns = ["id", "name", "price", "available", "description", "main_category", "sub_category", "ratings", "no_of_ratings", "image_url"]
    
    sell_df = pd.read_csv('db/generated/Sells.csv', header=None)
    sell_df.columns = ["sid", "pid", "quantity"]
    
    feedback = pd.read_csv('db/generated/Feedbacks.csv', header=None)
    feedback.columns = ["id", "uid", "pid", "comment", "rating", "comment_time"]
    
    prod_quants = sell_df.groupby("pid").agg({"quantity": "sum"})
    
    avg_ratings = feedback.groupby("pid").agg({"rating": "mean"})
    num_ratings = feedback.groupby("pid").agg({"rating": "sum"})
    
    with open('db/generated/Products.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Products...', end=' ', flush=True)
        for pid in range(len(prod_df)):
            if pid % 100 == 0:
                print(f'{pid}', end=' ', flush=True)
            
            name = prod_df["name"].iloc[pid]
            price = prod_df["price"].iloc[pid]
            if pid in prod_quants.index:
                quantity = prod_quants.loc[pid].values[0]
            else:
                quantity = 0
                
            if pid in avg_ratings.index:
                rating = avg_ratings.loc[pid].values[0]
            else:
                rating = 0
                
            if pid in num_ratings.index:
                no_of_ratings = num_ratings.loc[pid].values[0]
            else:
                no_of_ratings = 0
            
                
            description = prod_df["description"].iloc[pid]
            main_category = prod_df["main_category"].iloc[pid]
            sub_category = prod_df["sub_category"].iloc[pid]
            
            
            no_of_ratings = prod_df["no_of_ratings"].iloc[pid]
            image_url = prod_df["image_url"].iloc[pid]
            
            writer.writerow([pid, name, price, quantity, description, main_category, sub_category, rating, no_of_ratings, image_url])
            
        print(f'{num_products} generated; {len(available_pids)} available')
    return available_pids


def gen_purchases(num_purchases, available_pids):
    df = pd.read_csv('db/generated/Sells.csv', header=None)
    df.columns = ["sid", "pid", "quantity"]

    prev_tuples = set([])
    
    with open('db/generated/Purchases.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Purchases...', end=' ', flush=True)
        for id in range(num_purchases):
            if id % 100 == 0:
                print(f'{id}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
        
            row = df.sample(n=1)
            sid, pid = int(row["sid"].iloc[0]), int(row["pid"].iloc[0])
            quantity = random.randint(1, row["quantity"].iloc[0]-1)
            fulfillment = random.choice([True, False])  # Random boolean for fulfillment

            
            time_purchased = fake.date_time()
            
            if (uid, pid, sid, time_purchased) not in prev_tuples:
                prev_tuples.add((uid, pid, sid, time_purchased)) 
                writer.writerow([id, uid, pid, sid, time_purchased, quantity, fulfillment])
        print(f'{num_purchases} generated')
    return

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


def gen_sellers_and_sells(): 
    users_df = pd.read_csv('Users.csv', index_col = None)
    products_df = pd.read_csv('Products.csv', index_col = None)
    
    # get 0th col of users and products as IDs 
    user_ids = users_df.iloc[:, 0].tolist()
    product_ids = products_df.iloc[:, 0].tolist()
    
    # 9.7 sellers / 310 users = 3.12% percent of users are sellers on Amazon based on data from Google 
    # randomly select 3.12% of users to be sellers as well 
    num_sellers = math.ceil(0.0312 * len(user_ids))
    selling_users = random.sample(user_ids, num_sellers)
    
    # create a sellers.csv from users with all the sellers in sample 
    sellers_df = pd.DataFrame(selling_users)
    sellers_df.to_csv('Sellers.csv', index=False, header=False)
    
    random.shuffle(product_ids)
    
    combinations = []
    
    # for every product, ensure it has only one seller 
    for i, product_id in enumerate(product_ids):
        seller = selling_users[i % num_sellers] # cycle through sellers for uniform ish distribution
        combinations.append((seller, product_id, random.randint(7, 20))) # seller, product id, quantity between 7 and 20 

    sales_df = pd.DataFrame(combinations) # two columns: sellers, product id they sell 
    
    sales_df.to_csv('Sells.csv', index=False, header = False)

def get_user_ids():
    user_ids = set()
    with open('Users.csv', 'r') as f:
        reader = csv.reader(f)
        next(reader)  
        for row in reader:
            user_ids.add(row[0])  
    return user_ids

def gen_sfeedbacks(num_feedbacks, num_sellers):
    with open('Sellers.csv', 'r') as f:
        sellers = list(csv.reader(f))
    
    user_ids = get_user_ids() 
    feedback_combinations = set()  
    feedbacks_written = 0
    
    with open('SellerFeedbacks.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Seller Feedbacks...', end=' ', flush=True)
        
        while feedbacks_written < num_feedbacks:
            seller = fake.random_element(elements=sellers)
            sid = seller[0]  
            uid = fake.random_element(elements=user_ids)  
            
            if (uid, sid) in feedback_combinations:
                continue 
            
            feedback_combinations.add((uid, sid))
            feedback_id = feedbacks_written
            comment = fake.sentence()
            rating = fake.random_int(min=1, max=5)
            feedback_time = fake.date_time_this_decade(before_now=True, after_now=False)
            
            writer.writerow([feedback_id, sid, uid, comment, rating, feedback_time.strftime('%Y-%m-%d %H:%M:%S')])
            feedbacks_written += 1
            if feedbacks_written % 100 == 0:
                print(f'{feedbacks_written}', end=' ', flush=True)
        
        print(f'{feedbacks_written} generated.')

def get_csv_writer(file_handle):
    # Configure the CSV writer to avoid quoting non-string values
    return csv.writer(file_handle, quoting=csv.QUOTE_MINIMAL)
def gen_cart_data(num_cart_entries, num_products, num_users):
    with open('Cart.csv', 'w', newline='') as f:
        writer = get_csv_writer(f)
        print('Cart data...', end=' ', flush=True)
        
        my_set = set()  # Use an empty set for uniqueness
        product_ids = range(num_products)  # Create a range of product IDs (0 to num_products - 1)
        
        for entry_id in range(num_cart_entries):
            uid = fake.random_int(min=0, max=num_users - 1)
            pid = fake.random_element(elements=product_ids)  # Random product ID from the iterable

            if (uid, pid) not in my_set:
                my_set.add((uid, pid))
                quantity = fake.random_int(min=1, max=10)  # Random quantity between 1 and 10
                writer.writerow([uid, pid, quantity])
        
        print(f'{len(my_set)} cart entries generated')  # Use `len(my_set)` to reflect actual unique entries



# gen_users(num_users)
# gen_purchases(num_purchases, available_pids)
# gen_feedbacks(num_feedbacks)
# gen_sellers_and_sells()
gen_products()


# gen_sfeedbacks(400, num_sellers)
# num_cart_entries = 500  # Adjust as needed
# gen_cart_data(num_cart_entries, num_products, num_users)