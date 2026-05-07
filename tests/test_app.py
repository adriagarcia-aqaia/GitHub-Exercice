import pytest


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code in (307, 302)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, dict)
    assert "Chess Club" in body
    assert "participants" in body["Chess Club"]


def test_signup_for_existing_activity_succeeds(client):
    email = "new.student@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"


@pytest.mark.parametrize("method", ["post", "delete"])
def test_activity_not_found_returns_404(client, method):
    if method == "post":
        response = client.post(
            "/activities/Unknown Activity/signup",
            params={"email": "student@mergington.edu"},
        )
    else:
        response = client.delete(
            "/activities/Unknown Activity/participants",
            params={"email": "student@mergington.edu"},
        )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_duplicate_signup_returns_400(client):
    existing_email = "michael@mergington.edu"

    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_without_email_returns_422(client):
    response = client.post("/activities/Chess Club/signup")

    assert response.status_code == 422


def test_unregister_participant_succeeds(client):
    existing_email = "james@mergington.edu"

    response = client.delete(
        "/activities/Basketball Team/participants",
        params={"email": existing_email},
    )

    assert response.status_code == 200
    assert response.json()["message"] == (
        f"Unregistered {existing_email} from Basketball Team"
    )


def test_unregister_unknown_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "missing.student@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"


def test_unregister_without_email_returns_422(client):
    response = client.delete("/activities/Chess Club/participants")

    assert response.status_code == 422
