
# truckTable

| Field Name      | Description                        | Data Type | Example     | Source           |
|-----------------|------------------------------------|-----------|-------------|------------------|
| truckID         | Unique identifier for the truck    | TEXT      | TR01        | User entered     |
| make            | Manufacturer of the truck          | TEXT      | Volvo       | User entered     |
| model           | Model of the truck                 | TEXT      | FH16        | User entered     |
| size            | Size category of the truck         | TEXT      | XL          | User entered     |
| truckSupplierID | Supplier's unique ID               | TEXT      | SUP001      | User entered     |
| buyingPrice     | Purchase price of the truck        | FLOAT     | 25000.00    | User entered     |
| sellingPrice    | Sale price of the truck            | FLOAT     | 32000.00    | User entered     |
| stockLevel      | Number of trucks in stock          | INTEGER   | 10          | User entered     |
| reorderLevel    | Stock level to trigger reorder     | INTEGER   | 3           | User entered     |
| reorderAmount   | Amount to reorder when low         | INTEGER   | 5           | User entered     |

# supplierTable

| Field Name      | Description                        | Data Type | Example           | Source           |
|-----------------|------------------------------------|-----------|-------------------|------------------|
| supplierID      | Unique identifier for the supplier | TEXT      | SUP001            | User entered     |
| supplierName    | Name of the supplier               | TEXT      | TruckSupplies Ltd | User entered     |
| supplierAddress | Address of the supplier            | TEXT      | 123 Main St       | User entered     |
| supplierPhone   | Phone number of the supplier       | TEXT      | 01234567890       | User entered     |
| supplierEmail   | Email address of the supplier      | TEXT      | info@trucks.com   | User entered     |

# customerTable

| Field Name      | Description                        | Data Type | Example           | Source           |
|-----------------|------------------------------------|-----------|-------------------|------------------|
| customerID      | Unique identifier for the customer | TEXT      | CUST01            | User entered     |
| customerName    | Name of the customer               | TEXT      | John Smith        | User entered     |
| customerAddress | Address of the customer            | TEXT      | 456 Oak Ave       | User entered     |
| customerPhone   | Phone number of the customer       | TEXT      | 09876543210       | User entered     |
| customerEmail   | Email address of the customer      | TEXT      | john@email.com    | User entered     |

# orderTable

| Field Name        | Description                          | Data Type | Example   | Source           |
|-------------------|--------------------------------------|-----------|-----------|------------------|
| orderID           | Unique identifier for the order      | TEXT      | ORD001    | User entered     |
| orderCustomerID   | Customer who placed the order        | TEXT      | CUST01    | User entered     |
| orderDate         | Date the order was placed            | TEXT      | 2025-09-12| User entered     |
| paid              | Whether the order is paid (Y/N)      | TEXT      | Y         | User entered     |

# orderItemsTable

| Field Name         | Description                          | Data Type | Example   | Source           |
|--------------------|--------------------------------------|-----------|-----------|------------------|
| orderItemsOrderID  | Order ID for the item                | TEXT      | ORD001    | User entered     |
| orderItemstruckID  | Truck ID for the item                | TEXT      | TR01      | User entered     |
| quantity           | Quantity of trucks in the order      | INTEGER   | 2         | User entered     |
