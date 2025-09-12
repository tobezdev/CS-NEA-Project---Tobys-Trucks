-- Test data for truckTable
INSERT INTO truckTable VALUES ('TR01', 'Volvo', 'FH16', 'XL', 'SUP001', 25000.00, 32000.00, 10, 3, 5);
INSERT INTO truckTable VALUES ('TR02', 'Scania', 'R500', 'L', 'SUP002', 22000.00, 29500.00, 7, 2, 4);
INSERT INTO truckTable VALUES ('TR03', 'Mercedes', 'Actros', 'M', 'SUP003', 21000.00, 28000.00, 5, 2, 3);
INSERT INTO truckTable VALUES ('TR04', 'DAF', 'XF', 'L', 'SUP001', 23000.00, 31000.00, 8, 3, 4);
INSERT INTO truckTable VALUES ('TR05', 'MAN', 'TGX', 'XL', 'SUP002', 24000.00, 32500.00, 6, 2, 5);

-- Test data for supplierTable
INSERT INTO supplierTable VALUES ('SUP001', 'TruckSupplies Ltd', '123 Main St', '01234567890', 'info@trucks.com');
INSERT INTO supplierTable VALUES ('SUP002', 'HaulageParts Inc', '456 Oak Ave', '09876543210', 'contact@haulage.com');
INSERT INTO supplierTable VALUES ('SUP003', 'EuroTruckers', '789 Birch Rd', '01112223344', 'sales@eurotruckers.com');
INSERT INTO supplierTable VALUES ('SUP004', 'BigRig Depot', '1010 Cedar Blvd', '01555666777', 'support@bigrig.com');
INSERT INTO supplierTable VALUES ('SUP005', 'FleetSource', '2020 Spruce Ln', '01333444555', 'hello@fleetsource.com');

-- Test data for customerTable
INSERT INTO customerTable VALUES ('CUST01', 'John Smith', '789 Pine Rd', '07700111222', 'john@email.com');
INSERT INTO customerTable VALUES ('CUST02', 'Jane Doe', '321 Maple St', '07700333444', 'jane@email.com');
INSERT INTO customerTable VALUES ('CUST03', 'Bob Brown', '654 Elm St', '07700555666', 'bob@email.com');
INSERT INTO customerTable VALUES ('CUST04', 'Alice Green', '987 Willow Ave', '07700777888', 'alice@email.com');
INSERT INTO customerTable VALUES ('CUST05', 'Charlie Black', '159 Oak Dr', '07700999000', 'charlie@email.com');

-- Test data for orderTable
INSERT INTO orderTable VALUES ('ORD001', 'CUST01', '2025-09-12', 'Y');
INSERT INTO orderTable VALUES ('ORD002', 'CUST02', '2025-09-10', 'N');
INSERT INTO orderTable VALUES ('ORD003', 'CUST03', '2025-09-09', 'Y');
INSERT INTO orderTable VALUES ('ORD004', 'CUST04', '2025-09-08', 'N');
INSERT INTO orderTable VALUES ('ORD005', 'CUST05', '2025-09-07', 'Y');

-- Test data for orderItemsTable
INSERT INTO orderItemsTable VALUES ('ORD001', 'TR01', 2);
INSERT INTO orderItemsTable VALUES ('ORD002', 'TR02', 3);
INSERT INTO orderItemsTable VALUES ('ORD003', 'TR03', 1);
INSERT INTO orderItemsTable VALUES ('ORD004', 'TR05', 1);
INSERT INTO orderItemsTable VALUES ('ORD005', 'TR01', 1);
