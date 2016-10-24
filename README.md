# async-rest
Tornado REST API web server example.

Can asynchronously compute primes, factorize numbers and ping servers.

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
    **Content:** `{ error : "Please, provide a username param." }`
    
    
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
    **Content:** `{ error : "Please, provide a username param." }`
