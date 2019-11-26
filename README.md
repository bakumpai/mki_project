## Installing
Install `python` at least version `3.6`, download [here](https://www.python.org) 

After python installed, Follow this instructions
```bash
git clone https://github.com/bakumpai/mki_project
python3 initdb.py
env FLASK_APP=main.py flask run
```

## API Endpoint
These endpoints allow you to get a useful data about teaching assistant of some course
## GET
`http://localhost:5000`[/api/v1/teaching_assistant](#get-apiv1teaching_assistant) <br/>
`http://localhost:5000`[/api/v1/users](#get-apiv1users) <br/>

## POST
`http://localhost:5000`[/api/v1/teaching_assistant](#/api/v1/teaching_assistant) <br/>
`http://localhost:5000`[/api/v1/users](#/api/v1/users) <br/>
___
### GET /api/v1/teaching_assistant
Get teaching assistant information for a given course name and the year of the course

**Parameters**

|          Name | Required |  Type   | Description                                                                                                                                                           |
| -------------:|:--------:|:-------:| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|     `course` | required | -  | It contains name and year of the course
|     `name` | required | List  | List of course name. <br/><br/> No need to write full name of the course, your can just write first word or last word of the course's name.<br/><br/> Example : ["CS11","Winter"]
|     `year` | required | Integer  | Year of the course.<br/><br/> Every course has year attribute, it useful for identifying the certain course by their year.<br/><br/>CS1121 Data Structure & Algorithm Winter 2015, it means DSA course for Winter 2015 and it has different teaching assistant than DSA Winter 2020

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

___
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

___
### POST /api/v1/teaching_assistant
It has secret feature, we think you don't need to know about it, it's none of your business and has nothing to do with you anyway.

**Response**

```
//It is what you'll get if you insist to access it using POST request
{
    "message": "You're not authenticated to send such a request."
}
```

___
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
	"_options":"add"
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

