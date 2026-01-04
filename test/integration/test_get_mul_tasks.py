def test_get_one_task_by_id(client, create_user, create_task, default_start_test_sequence):

    response = client.get("/get/2")
    assert response.status_code == 200
    assert response.json() == {
        "task": {
                "user_id": 1,
                "task_content": "Second task",
                "is_complete": False,
                "id": 2
            }
        }
    
def test_get_all_tasks(client, create_task, create_user):
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
    
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "tasks": [
                {
                    "user_id": 1,
                    "task_content": "First task",
                    "is_complete": False,
                    "id": 1
                },
                {
                    "user_id": 1,
                    "task_content": "Second task",
                    "is_complete": False,
                    "id": 2
                },
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
                {
                    "user_id": 1,
                    "task_content": "5th task",
                    "is_complete": False,
                    "id": 5
                },
                {
                    "user_id": 1,
                    "task_content": "6th task",
                    "is_complete": False,
                    "id": 6
                },
            ],
        }
    

def test_get_task_403_error(client, create_user, create_task, default_start_test_sequence):

    second_default_user = create_user(
        username="user2",
        password="123"
    )

    client.cookies["access_token"] = second_default_user["token"]

    response = client.get("/get/1/")
    assert response.status_code == 403
    assert response.json() == {
            "detail":"User with id=2 do not have access to the task with id=1",
            }

def test_get_task_404_error(client, create_user, create_task):
    default_user = create_user(
        username="user",
        password="123"
    )

    response = client.get("/delete/99/",
                          params=[
                              ("task_content", "Changed content")
                          ])
    assert response.status_code == 404
    assert response.json() == {
            "detail":"Task with id=99 not found",
            }
