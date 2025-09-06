import psycopg2
import os
# from dotenv import load_dotenv
# load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT")
)

# Prompt user for product details
def get_product_info():
    name = input("Enter product name (required): ").strip()
    while not name:
        name = input("Product name cannot be empty. Enter product name: ").strip()
    price = input("Enter product price (required): ").strip()
    while True:
        try:
            price = float(price)
            break
        except ValueError:
            price = input("Invalid price. Enter a numeric value for price: ").strip()
    description = input("Enter product description (optional): ").strip() or None
    size = input("Enter product size (optional): ").strip() or None
    return name, price, description, size

def main():
    name, price, description, size = get_product_info()
    print(f"\nYou entered:\n  Name: {name}\n  Price: {price}\n  Description: {description}\n  Size: {size}")
    confirm = input("\nProceed to insert this product into the database? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Aborted.")
        return
    try:
        conn = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO products (name, price, description, size)
            VALUES (%s, %s, %s, %s)
            RETURNING id;
            """,
            (name, price, description, size)
        )
        product_id = cur.fetchone()[0]
        conn.commit()
        print(f"\nProduct inserted successfully with ID: {product_id}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()
