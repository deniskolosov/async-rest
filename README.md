# async-rest
Tornado REST API web server example.

Can asynchronously compute primes, factorize numbers and ping servers.

###Install requirements
``` bash
$ pip install -r requirements.txt
```

###Run server
``` bash
$ python server.py --port=<port_number>
```

default port number is `:8080`

Now you can use curl or your web browser to `GET` API methods.
Note you have to provide `username` query parameter.

### Example:
request
```
http://localhost:8080/api/ping?&server=google.com&ping_count=1&username=denis
```

will result in

```
{"result": [{"try": 1, "ret_code": 0}]}
```

request
```
http://localhost:8080/api/primes/42?username=denis
```

will result in

```
{"result": 181}
```

request 
```
http://localhost:8080/api/factorize/57543?username=denis
```

will result in

```
{"result": [3, 19181]}
```

###Rest API methods:

**Compute prime**
----
 Computes n-th prime number

* **URL**

  /api/primes/:n

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `n=[integer]`

* **Data Params**


   **Required:**
 
   `username=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"result": 3203}`
 
* **Error Response:**

  * **Code:** 400: <br />
    **Content:** `{ error : "Please, provide a username param." }`
    
    
**Factorize number**
----
 Factorize number to prime components

* **URL**

  /api/factorize/:number

* **Method:**

  `GET`
  
*  **URL Params**

   **Required:**
 
   `number=[integer]`

* **Data Params**

    **Required:**
   `username=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"result": [2, 293]}`
 
* **Error Response:**

  * **Code:** 400: Bad Request <br />
    **Content:** `{"error": {"message": "Bad Request", "code": 400}}`
    
    
**Ping server**
----
  Ping provided hostname n times

* **URL**

  /api/ping

* **Method:**

  `GET`
  
*  **URL Params**

    None
     

* **Data Params**

    **Required:**
   `server=[string]`
   `ping_count=[integer]`
   `username=[string]`

* **Success Response:**

  * **Code:** 200 <br />
    **Content:** `{"result": [{"try": 1, "ret_code": 0}, {"try": 2, "ret_code": 0}]}`
 
* **Error Response:**

  * **Code:** 400: Bad Request <br />
    **Content:** `{"error": {"message": "Bad Request", "code": 400}}`
