<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/kajuberdut/aiosql-mysql">
    <img src="https://raw.githubusercontent.com/kajuberdut/aiosql-mysql/main/images/logo.svg" alt="Logo" width="160" height="160">
  </a>

  <h2 align="center">aiosql-mysql</h2>

</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
    </li>
    <li><a href="#usage">Usage</a>
      <!-- <ul>
        <li><a href="#further-examples">Further Examples</a></li>
      </ul> -->
    </li>
    <!-- <li><a href="#roadmap">Roadmap</a></li> -->
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#thanks">Thanks</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

aiosql-mysql is a database adaptor intended to allow the use of [asyncmy](https://github.com/long2ice/asyncmy) with [aiosql](https://github.com/nackjicholson/aiosql).


### Warning:
This project is in early developement. The PyMySQL adaptor works but is not fully tested. AsyncMy is not implimented and working at this time, please check back later.


<!-- GETTING STARTED -->
## Getting Started

<!-- To get a local copy up and running follow these simple steps. -->
<!-- ### Installing with pip -->
  <!-- ```sh
  pip install aiosql-mysql
  ``` -->

For information about cloning and dev setup see: [Contributing](#Contributing)


<!-- USAGE EXAMPLES -->
## Usage
This is example is adapted from aiosql's readme.

*users.sql*

```sql

-- name: get-user-by-username^
SELECT *
FROM users
WHERE username = :username;

-- name: create_users#
CREATE TABLE users ( userid INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                     username VARCHAR(100),
                     firstname VARCHAR(100),
                     lastname VARCHAR(100)
);

-- name: insert_bob!
INSERT INTO users (username, firstname, lastname)
VALUES ('bob', 'bob', 'smith');

```

### Blocking execution
Indexing a document adds it to or updates it in the search store.
```python
import aiosql
import pymysql
from aiosql_mysql import PyMySQLAdaptor

conn = pymysql.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="password",
        database="ExampleDb",
        cursorclass=pymysql.cursors.DictCursor,
    )

queries = aiosql.from_path("./greetings.sql", PyMySQLAdaptor)
queries.create_users(conn)
queries.insert_bob(conn)
result = queries.get_user_by_username(conn, username="bob")
print(result)
# {'userid': 1, 'username': 'bob', 'firstname': 'bob', 'lastname': 'smith'}

```

### Async execution
**Coming Soon**

<!-- CONTRIBUTING -->
## Contributing
See the [open issues](https://github.com/kajuberdut/aiosql-mysql/issues) for a list of proposed features (and known issues).

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
<!-- 3. Add tests, we aim for 100% test coverage [Using Coverage](https://coverage.readthedocs.io/en/coverage-5.3.1/#using-coverage-py) -->
4. execute: py.test --cov-report xml:cov.xml --cov
5. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
6. Push to the Branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Cloning / Development setup
1. Clone the repo and install
    ```sh
    git clone https://github.com/kajuberdut/aiosql-mysql.git
    cd aiosql-mysql
    pipenv install --dev
    ```
2. Run tests
    ```sh
    pipenv shell
    py.test
    ```
  For more about pipenv see: [Pipenv Github](https://github.com/pypa/pipenv)



<!-- LICENSE -->
## License

Distributed under the UnLicense. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Patrick Shechet - patrick.shechet@gmail.com

Project Link: [https://github.com/kajuberdut/aiosql-mysql](https://github.com/kajuberdut/aiosql-mysql)


<!-- THANKS -->
## Thanks
This library would be pointless without:
- [Will Vaughn, creator of aiosql](https://github.com/nackjicholson)
- [The other contributors to aiosql](https://github.com/nackjicholson/aiosql/graphs/contributors)
- [The PyMySql Team](https://github.com/PyMySQL/PyMySQL)
- [Long2Ice, creator of asyncmy](https://github.com/long2ice)
- [The aiomysql team who's work makes asyncmy possible](https://github.com/aio-libs/aiomysql/graphs/contributors)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/kajuberdut/aiosql-mysql.svg?style=for-the-badge
[contributors-url]: https://github.com/kajuberdut/aiosql-mysql/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/kajuberdut/aiosql-mysql.svg?style=for-the-badge
[forks-url]: https://github.com/kajuberdut/aiosql-mysql/network/members
[stars-shield]: https://img.shields.io/github/stars/kajuberdut/aiosql-mysql.svg?style=for-the-badge
[stars-url]: https://github.com/kajuberdut/aiosql-mysql/stargazers
[issues-shield]: https://img.shields.io/github/issues/kajuberdut/aiosql-mysql.svg?style=for-the-badge
[issues-url]: https://github.com/kajuberdut/aiosql-mysql/issues
[license-shield]: https://img.shields.io/badge/License-unlicense-orange.svg?style=for-the-badge
[license-url]: https://github.com/kajuberdut/aiosql-mysql/blob/main/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/patrick-shechet
