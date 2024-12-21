import csv
import random
from datetime import datetime, timedelta

columns = [
    "user_id", "name", "email", "gender", "age", "location", "account_creation_date", "last_login_date",
    "total_spent", "transaction_frequency", "average_transaction_value", "last_transaction_date",
    "number_of_transactions", "favorite_payment_method", "purchase_channel", "preferred_device",
    "preferred_language", "time_on_site", "page_views_per_session", "average_cart_value",
    "abandoned_cart_count", "product_browsing_history", "loyalty_program_member", "loyalty_points_balance",
    "email_open_rate", "email_click_rate", "SMS_opt_in", "SMS_click_rate", "best_time_in_the_day",
    "best_day_in_a_week", "best_week_in_a_month", "coupon_usage_frequency", "social_media_engagement",
    "number_of_reviews_written", "average_review_rating", "referral_count", "customer_service_interactions",
    "live_chat_use_frequency", "marketing_segment", "campaign_engagement_score", "preferred_communication_channel",
    "click_through_rate", "conversion_rate", "discount_usage_rate", "preferred_brand", "brand_loyalty_index",
    "lifetime_value_estimate", "frequency_of_visits_per_week", "returning_customer", "shopping_basket_value",
    "cart_conversion_rate", "purchase_value_category", "transaction_frequency_category", "product_affinity",
    "discount_affinity"
]

# dummy data
data = []
for i in range(1, 6):  # Create 5 rows of data
    data.append([
        i,  # user_id
        f"User {i}",  # name
        f"user{i}@example.com",  # email
        random.choice(["Male", "Female", "Other"]),  # gender
        random.randint(18, 65),  # age
        random.choice(["New York", "London", "Tokyo", "Sydney"]),  # location
        (datetime.now() - timedelta(days=random.randint(1, 1000))).strftime("%Y-%m-%d"),  # account_creation_date
        (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),  # last_login_date
        round(random.uniform(100, 10000), 2),  # total_spent
        random.randint(1, 50),  # transaction_frequency
        round(random.uniform(10, 500), 2),  # average_transaction_value
        (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d"),  # last_transaction_date
        random.randint(1, 100),  # number_of_transactions
        random.choice(["Credit Card", "PayPal", "Bank Transfer"]),  # favorite_payment_method
        random.choice(["Online", "In-store"]),  # purchase_channel
        random.choice(["Mobile", "Desktop", "Tablet"]),  # preferred_device
        random.choice(["English", "Spanish", "French", "German"]),  # preferred_language
        random.randint(1, 500),  # time_on_site
        random.randint(1, 20),  # page_views_per_session
        round(random.uniform(50, 300), 2),  # average_cart_value
        random.randint(0, 10),  # abandoned_cart_count
        "Product1, Product2",  # product_browsing_history
        random.choice([True, False]),  # loyalty_program_member
        random.randint(0, 1000),  # loyalty_points_balance
        round(random.uniform(0, 100), 2),  # email_open_rate
        round(random.uniform(0, 50), 2),  # email_click_rate
        random.choice([True, False]),  # SMS_opt_in
        round(random.uniform(0, 30), 2),  # SMS_click_rate
        random.choice(["Morning", "Afternoon", "Evening"]),  # best_time_in_the_day
        random.choice(["Monday", "Friday", "Sunday"]),  # best_day_in_a_week
        random.randint(1, 4),  # best_week_in_a_month
        round(random.uniform(0, 1), 2),  # coupon_usage_frequency
        round(random.uniform(0, 1), 2),  # social_media_engagement
        random.randint(0, 10),  # number_of_reviews_written
        round(random.uniform(1, 5), 1),  # average_review_rating
        random.randint(0, 10),  # referral_count
        random.randint(0, 20),  # customer_service_interactions
        random.randint(0, 10),  # live_chat_use_frequency
        random.choice(["High-Value", "New Customer", "Loyal Customer"]),  # marketing_segment
        random.randint(1, 100),  # campaign_engagement_score
        random.choice(["Email", "SMS", "Push Notification"]),  # preferred_communication_channel
        round(random.uniform(0, 10), 2),  # click_through_rate
        round(random.uniform(0, 10), 2),  # conversion_rate
        round(random.uniform(0, 10), 2),  # discount_usage_rate
        random.choice(["Brand A", "Brand B", "Brand C"]),  # preferred_brand
        random.randint(0, 100),  # brand_loyalty_index
        round(random.uniform(1000, 50000), 2),  # lifetime_value_estimate
        random.randint(0, 7),  # frequency_of_visits_per_week
        random.choice([True, False]),  # returning_customer
        round(random.uniform(10, 1000), 2),  # shopping_basket_value
        round(random.uniform(0, 1), 2),  # cart_conversion_rate
        random.choice(["High", "Medium", "Low"]),  # purchase_value_category
        random.choice(["Frequent", "Occasional", "Rare"]),  # transaction_frequency_category
        "ProductA, ProductB",  # product_affinity
        random.randint(0, 5)  # discount_affinity
    ])

csv_file = "../user_attributes.csv"
with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(columns)
    writer.writerows(data)

print(f"CSV file '{csv_file}' created successfully.")
