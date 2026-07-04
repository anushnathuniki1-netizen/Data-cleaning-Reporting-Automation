import pandas as pd
import matplotlib.pyplot as plt
import os

# Create charts folder
os.makedirs("charts", exist_ok=True)

# Read CSV file
df = pd.read_csv("sales_data.csv")

print("\n===== ORIGINAL DATA =====\n")
print(df.to_string(index=False))

# Remove duplicate rows
df = df.drop_duplicates()

# Fill missing values
df = df.fillna({
    "Customer": "Unknown",
    "City": "Unknown",
    "Sales": df["Sales"].mean()
})

# Save cleaned data
df.to_csv("cleaned_data.csv", index=False)

# Create Summary Report
with open("summary.txt", "w") as file:
    file.write("DATA CLEANING REPORT\n")
    file.write("=========================\n")
    file.write(f"Total Records : {len(df)}\n")
    file.write(f"Total Columns : {len(df.columns)}\n")
    file.write(f"Missing Values : {df.isnull().sum().sum()}\n")
    file.write(f"Duplicate Records : {df.duplicated().sum()}\n")

# Create Excel Report
with pd.ExcelWriter("report.xlsx", engine="openpyxl") as writer:
    df.to_excel(writer, sheet_name="Cleaned Data", index=False)

    summary = pd.DataFrame({
        "Metric": [
            "Total Records",
            "Total Columns",
            "Missing Values",
            "Duplicate Records"
        ],
        "Value": [
            len(df),
            len(df.columns),
            df.isnull().sum().sum(),
            df.duplicated().sum()
        ]
    })

    summary.to_excel(writer, sheet_name="Summary", index=False)

# Chart 1 - Sales by City
sales = df.groupby("City")["Sales"].sum()

plt.figure(figsize=(6,4))
sales.plot(kind="bar")
plt.title("Total Sales by City")
plt.xlabel("City")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("charts/sales_chart.png")
plt.close()

# Chart 2 - Customer Distribution
customers = df["City"].value_counts()

plt.figure(figsize=(6,6))
customers.plot(kind="pie", autopct="%1.1f%%")
plt.title("Customer Distribution by City")
plt.ylabel("")
plt.tight_layout()
plt.savefig("charts/customer_chart.png")
plt.close()

print("\n===== PROJECT COMPLETED SUCCESSFULLY =====")
print("Files Created:")
print("1. cleaned_data.csv")
print("2. report.xlsx")
print("3. summary.txt")
print("4. charts/sales_chart.png")
print("5. charts/customer_chart.png")

