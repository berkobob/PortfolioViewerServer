# Portfolio Viewer

Manage lists of stock portfolios for multiple users. Uses client server model. This is the server. Requests served via http REST API

## Model

Use an API to hide the implementation of the data model althought it'll just be a python package.

### Possible implementations

* MySQL
* NoSQL
* Flat files

### API

FUNCTION | PORT | STOCK
---------|------|------
Create   |      |
Read     |      |
Update?  |      |
Delete   |      |

* [ ] To do
* [x] Done

* Create
  * portfolio
  * new stock in portfolio
* Read
  * list of ports
  * list of stocks
* Update
* Delete

- - -

## Controller

Contains all logic. Inclding price updating engine.
Include function to register listeners so that prices are only updated when a listener is registered then, when a price changes, listeners are notified.

### Functionality

* Upload portfolio
* Delete portfolio
* Create empty portfolio
* Portfolio performance?
* Add share
* Delete share
