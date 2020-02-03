# robotframework-historic-parser

Parser to push robotframework execution results to MySQL (for Robotframework Historic report)

![PyPI version](https://badge.fury.io/py/robotframework-historic-parser.svg)
[![Downloads](https://pepy.tech/badge/robotframework-historic-parser)](https://pepy.tech/project/robotframework-historic-parser)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![Open Source Love png1](https://badges.frapsoft.com/os/v1/open-source.png?v=103)
[![HitCount](http://hits.dwyl.io/adiralashiva8/robotframework-historic-parser.svg)](http://hits.dwyl.io/adiralashiva8/robotframework-historic-parser)

---

## Installation

 - Install `robotframework-historic-parser` 

    ```
    pip install robotframework-historic-parser
    ```

--- 

## Usage

   Robotframework Historic report required following information, users must pass respective info while using parser

    -o --> output.xml file name
    -s --> mysql hosted machine ip address (default: localhost)
    -u --> mysql user name (default: superuser)
    -p --> mysql password (default: passw0rd)
    -n --> project name in robotframework historic
    -e --> execution info

 - Use `robotframework-historic-parser` to parse output.xml's

   ```
   > rfhistoricparser
    -o "OUTPUT.xml FILE"
    -s "<SQL_HOSTED_IP:3306>"
    -u "<NAME>"
    -p "<PWD>"
    -n "<PROJECT-NAME>"
    -e "<EXECUTION-INFO>"
   ```

   __Example:__
   ```
   > rfhistoricparser
    -o "output1.xml"
    -s "10.30.2.150:3306"
    -u "admin"
    -p "Welcome1!"
    -n "projec1"
    -e "Smoke test on v1.0"
   ```

---

> For more info refer to [robotframework-historic](https://github.com/adiralashiva8/robotframework-historic)
