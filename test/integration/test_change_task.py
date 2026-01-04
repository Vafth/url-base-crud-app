def test_change_task_by_id(client, create_user, create_task, default_start_test_sequence):
    default_user, response_create_2_tasks = default_start_test_sequence

    response = client.get("/change/1",
                          params=[
                              ("task_content", "Changed content")
                          ])
    assert response.status_code == 200
    assert response.json() == {
            "message":"Task chenged successfully",
            "task": {
                "user_id": default_user["user_id"],
                "task_content": "Changed content",
                "complete": False,
                "id": 1,
            }}
    
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
                "tasks": [
                {
                    "user_id": 1,
                    "task_content": "Changed content",
                    "is_complete": False,
                    "id": 1
                },
                {
                    "user_id": 1,
                    "task_content": "Second task",
                    "is_complete": False,
                    "id": 2
                },]}
    
def test_change_task_404_error(client, create_user, create_task, default_start_test_sequence):
    response = client.get("/change/99",
                          params=[
                              ("task_content", "Changed content")
                          ])
    assert response.status_code == 404
    assert response.json() == {
            "detail":"Task with id=99 not found",
            }

def test_change_task_403_error(client, create_user, create_task, default_start_test_sequence):

    second_default_user = create_user(
        username="user2",
        password="123"
    )

    client.cookies["access_token"] = second_default_user["token"]

    response = client.get("/change/1",
                          params=[
                              ("task_content", "Changed content")
                          ])
    assert response.status_code == 403
    assert response.json() == {
            "detail":"User with id=2 do not have access to the task with id=1",
            }
