import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
# Sample data: Transactions
data = {
'Transaction': [
'Milk, Bread, Diaper',
'Bread, Diaper, Beer',
'Milk, Diaper, Beer',
'Bread, Milk, Diaper',
'Bread, Diaper',
'Milk, Bread, Diaper, Beer',
]
}
# Convert transactions into a DataFrame
df = pd.DataFrame(data)
# Preprocess the data into a one-hot encoded format
# Split the items and create a one-hot encoded DataFrame
transactions = df['Transaction'].str.get_dummies(sep=', ')
# Print the one-hot encoded DataFrame
print("One-Hot Encoded DataFrame:")
print(transactions)
# Apply the Apriori algorithm
frequent_itemsets = apriori(transactions, min_support=0.5, use_colnames=True)
# Print the frequent itemsets
print("\nFrequent Itemsets:")
print(frequent_itemsets)
# Generate association rules
rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.5)
# Print the association rules
print("\nAssociation Rules:")
print(rules)