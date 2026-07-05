import pandas as pd
from src.Database import engine

# Load Support Tickets
tickets_df = pd.read_sql(
    "SELECT * FROM support_tickets",
    engine
)

# Load Transactions
transactions_df = pd.read_sql(
    "SELECT * FROM transactions",
    engine
)

# Load QA Pairs
qa_df = pd.read_sql(
    "SELECT * FROM qa_pairs",
    engine
)

# Display Shapes
print("Support Tickets:", tickets_df.shape)
print("Transactions:", transactions_df.shape)
print("QA Pairs:", qa_df.shape)