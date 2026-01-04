def test_post_one_task_after_registration(client, create_task, create_user):
    admin_user = create_user(
        username="Admin",
        password="123",
        is_admin=True
    )

    response_create_1_task = create_task(
        token = admin_user["token"],
        params = [
            ("task_content", "First task"),
        ]
    )
    
    assert response_create_1_task.status_code == 201
    assert response_create_1_task.json() == {
        "message":"1 tasks created successfully",
            "tasks": [
                {
                    "user_id": 1,
                    "task_content": "First task",
                    "is_complete": False,
                    "id": 1
                },
            ]
    }

def test_post_4_tasks_after_registration(client, create_task, create_user):
    admin_user = create_user(
        username="Admin",
        password="123",
        is_admin=True
    )

    response_create_4_tasks = create_task(
        token = admin_user["token"],
        params = [
            ("task_content", "First task"), 
            ("task_content", "Second task"),
            ("task_content", "Third task"), 
            ("task_content", "4th task"),
        ]
    )
    assert response_create_4_tasks.status_code == 201
    assert response_create_4_tasks.json() == {
        "message":"4 tasks created successfully",
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
            ],
        }


def test_post_task_422_error(client, create_user):
    default_user = create_user(
        username="user",
        password="123"
    )

    response = client.get("/post/")
    assert response.status_code == 422
    assert response.json() == {
            "detail":"Content for the Task was not given",
            }
