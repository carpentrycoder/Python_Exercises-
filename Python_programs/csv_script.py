import csv
import getindianname as name
from random import choice, randint
from datetime import timedelta
from faker import Faker

# Initialize Faker for contact details
fake = Faker('en_IN')

# Define the CSV file headers
headers = [
    "Customer_ID",
    "Customer_Name",
    "Contact_Number",
    "Email",
    "City",
    "Loan_Type",
    "Loan_Amount",
    "Interest_Rate",
    "Loan_Term_Years",
    "Application_Date",
    "Approval_Date",
    "Disbursement_Date",
    "Repayment_Status",
    "Remarks"
]

# Define loan types and corresponding interest rates
loan_types = {
    "Commercial Vehicle Loan": 10.5,
    "Small Business Loan": 12.0,
    "Personal Loan": 14.0,
    "Gold Loan": 9.0
}

# Generate random data for the CSV file
num_records = 10000
records = []

for i in range(1, num_records + 1):
    # Generate random customer names using the `getindianname` library
    gender = choice(["male", "female"])
    if gender == "male":
        customer_name = name.male()
    else:
        customer_name = name.female()

    contact_number = fake.phone_number()
    email = fake.email()
    city = fake.city()
    loan_type = choice(list(loan_types.keys()))
    loan_amount = round(randint(100000, 1000000), -3)  # Loan amount between 1 lakh to 10 lakhs
    interest_rate = loan_types[loan_type]
    loan_term_years = randint(1, 5)  # Loan term between 1 to 5 years
    application_date = fake.date_this_decade(before_today=True, after_today=False)
    approval_date = fake.date_between(start_date=application_date, end_date=application_date + timedelta(days=15))
    disbursement_date = fake.date_between(start_date=approval_date, end_date=approval_date + timedelta(days=7))
    repayment_status = choice(["Current", "Overdue", "Closed"])
    remarks = ""

    # Add remarks for overdue accounts
    if repayment_status == "Overdue":
        remarks = choice([
            "Missed last payment",
            "Account under review",
            "Sent reminder notice"
        ])

    records.append([
        i,
        customer_name,
        contact_number,
        email,
        city,
        loan_type,
        loan_amount,
        interest_rate,
        loan_term_years,
        application_date,
        approval_date,
        disbursement_date,
        repayment_status,
        remarks
    ])

# Write the records to a CSV file
output_file = "shriram_finance_loan_data.csv"

with open(output_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(records)

print(f"CSV file '{output_file}' has been created with {num_records} records.")
