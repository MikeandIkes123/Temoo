--FIXME: inconsistent naming of variables id vs something like cid. For example, products has an "id" instead of a "pid". This may cause confusion when writing queries.


\COPY Users FROM 'Users.csv' WITH DELIMITER ',' NULL '' CSV
-- since id is auto-generated; we need the next command to adjust the counter
-- for auto-generation so next INSERT will not clash with ids loaded above:
SELECT pg_catalog.setval('public.users_id_seq',
                         (SELECT MAX(id)+1 FROM Users),
                         false);

-- \COPY Products FROM 'Products.csv' WITH DELIMITER ',' NULL '' CSV
-- SELECT pg_catalog.setval('public.products_id_seq',
--                          (SELECT MAX(id)+1 FROM Products),
--                          false);

\COPY Products FROM 'Amazon_Products.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.products_id_seq',
                         (SELECT MAX(id)+1 FROM Products),
                         false);

\COPY Purchases FROM 'Purchases.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.purchases_id_seq',
                         (SELECT MAX(id)+1 FROM Purchases),
                         false);

\COPY Feedbacks FROM 'Feedbacks.csv' WITH DELIMITER ',' NULL '' CSV
SELECT pg_catalog.setval('public.feedbacks_id_seq',
                         (SELECT MAX(id)+1 FROM Feedbacks),
                         false);

\COPY Sellers FROM 'Sellers.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Sells FROM 'Sells.csv' WITH DELIMITER ',' NULL '' CSV

\COPY Cart FROM 'Cart.csv' WITH DELIMITER ',' NULL '' CSV

\COPY sFeedbacks FROM 'SellerFeedbacks.csv' WITH DELIMITER ',' NULL '' CSV