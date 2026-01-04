def test_get_tasks_by_page(client, create_task, create_user):
    default_user = create_user(
        username="user",
        password="123"
    )

    response_create_6_tasks = create_task(
        token = default_user["token"],
        params = [
            ("task_content", "First task"),
            ("task_content", "Second task"),
            ("task_content", "Third task"),
            ("task_content", "4th task"),
            ("task_content", "5th task"),
            ("task_content", "6th task"),
        ]
    )
    assert response_create_6_tasks.status_code == 201
    
    response = client.get("/", params={"limit": 2,
                                       "page": 2})
    assert response.status_code == 200
    assert response.json() == {
        "tasks": [
                {
                    "user_id": 1,
                    "task_content": "Third task",
                    "is_complete": False,
                    "id": 3
                },
                {
                    "user_id": 1,
                    "task_content": "4th task",
                    "is_complete": False,
                    "id": 4
                },
            ],
        }
    
def test_get_tasks_by_page_and_compelete_value(client, create_task, create_user):
    default_user = create_user(
        username="user",
        password="123"
    )

    response_create_6_tasks = create_task(
        token = default_user["token"],
        params = [
            ("task_content", "First task"),
            ("task_content", "Second task"),
            ("task_content", "Third task"),
            ("task_content", "4th task"),
            ("task_content", "5th task"),
            ("task_content", "6th task"),
        ]
    )
    assert response_create_6_tasks.status_code == 201
    
    response = client.get("/switch/3/")
    assert response.status_code == 200

    response = client.get("/switch/6/")
    assert response.status_code == 200

    response = client.get("/", params=[
                                    ("only_complete", True),
                                    ("limit", 2),
                                    ("page", 1)
                                ])
    assert response.status_code == 200
    assert response.json() == {
        "tasks": [
                {
                    "user_id": 1,
                    "task_content": "Third task",
                    "is_complete": True,
                    "id": 3
                },
                {
                    "user_id": 1,
                    "task_content": "6th task",
                    "is_complete": True,
                    "id": 6
                },
            ],
        }
def test_get_tasks_by_page_and_compelete_value_422_error(client, create_task, create_user):
    default_user = create_user(
        username="user",
        password="123"
    )

    response = client.get("/",
                        params=[
                            ("only_complete",   True),
                            ("only_uncomplete", True),
                        ])
    assert response.status_code == 422
    assert response.json() == {"detail":"Unprocessable queries: cannot generate response when only_complete and only_uncomplete == True. For more info visit /help/"}

    response = client.get("/",
                        params=[
                            ("limit", 0),
                        ])
    assert response.status_code == 422
    assert response.json() == {"detail":"Unprocessable queries: cannot generate response when amount of tasks in page limit = 0. For more info visit /help/"}