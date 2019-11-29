## Teaching Assistant API

These endpoints allow you to get a useful data about teaching assistant of some course.
All API Endpoint follows RFC 7797 that rules about JSON Web Signature (JWS) Unencoded Payload Option.

## Installing

Install `python` at least version `3.6`, download [here](https://www.python.org)

After python installed, Follow this instructions

```bash
git clone https://github.com/bakumpai/mki_project
python3 initdb.py
env FLASK_APP=main.py flask run
```

## API Authorization

All API Endpoint contain Authorization such as Basic Authorization, username and password is

```
Username: admin
Password: project@MKI2019!
```

## API Endpoint

All API Endpoint served at:

```
Production API : http://15-mki.cs.ui.ac.id
```

---

### GET /api/v1/teaching_assistant

Get teaching assistant information for a given course name and the year of the course

**Request Example**

```
//Request data about teaching assistant for course with the name that contains Winter or Fall or CS11
{
    "course":
    {
      "name": ["Winter","Fall","CS11"],
      "year": 2019
       }
    }
}
```

**Response**

```
{
    "course": [
        {
            "id": 2,
            "name": "CS277 Winter",
            "teaching_assistant": {
                "id": 2,
                "name": "Anwar"
            },
            "year": 2019
        },
        {
            "id": 3,
            "name": "CS299 Fall",
            "teaching_assistant": {
                "id": 3,
                "name": "Budiman"
            },
            "year": 2019
        }
    ],
    "message": "success"
}

```

---

### GET /api/v1/users

Get all users data, don't need any parameters, just send a request and we will give you everything.

**Response**

```
{
    "message": "Success",
    "payload": [
        {
            "email": "satrio@example.com",
            "id": 1,
            "name": "satrio"
        },
        {
            "email": "nugroho@example.com",
            "id": 2,
            "name": "nugroho"
        },
        {
            "email": "lengkap@example.com",
            "id": 3,
            "name": "lengkap"
        }
    ]
}
```

---

### POST /api/v1/teaching_assistant

It has secret feature, we don't think you need to know about it, it's none of your business and has nothing to do with you anyway.

**Response**

```
//It is what you'll get if you insist to access it using POST request
{
    "message": "You're not authenticated to send such a request."
}
```

---

### POST /api/v1/users

With this feature, you can do anything to user's data. Update, delete, and adding new data, just do whatever you want with it. It's good right?

**Request Example**

```
//add data
{
	"data":
		{
		"name":"budi",
		"email":"dwad@gmail.com"
		},
	"options":"add"
}


```

**Response**

```
//response after successfully adding new data
{
    "message": "Success",
    "payload": {
        "email": "dwad@gmail.com",
        "id": 4,
        "name": "budi"
    }
}
```
