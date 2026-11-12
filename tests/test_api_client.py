from src.api_client import get_streaming_platforms, search_movie


def test_search_movie_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": [
            {
                "id": 27205,
                "title": "Inception",
                "release_date": "2010-07-15",
                "vote_average": 8.8,
                "overview": "A thief steals corporate secrets.",
            }
        ]
    }
    mocker.patch("src.api_client.requests.get", return_value=mock_response)

    result = search_movie("Inception")

    assert result["title"] == "Inception"
    assert result["rating"] == 8.8
    assert "error" not in result


def test_search_movie_no_results(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": []}
    mocker.patch("src.api_client.requests.get", return_value=mock_response)

    result = search_movie("Unknown")

    assert "error" in result


def test_get_streaming_platforms_success(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "results": {
            "ES": {
                "flatrate": [
                    {"provider_name": "Netflix"},
                    {"provider_name": "Amazon Prime Video"},
                ],
                "rent": [{"provider_name": "Apple TV"}],
                "buy": [],
            }
        }
    }
    mocker.patch("src.api_client.requests.get", return_value=mock_response)

    result = get_streaming_platforms(27205, "ES")

    assert "Netflix" in result["streaming"]
    assert "Apple TV" in result["rent"]
    assert result["buy"] == []


def test_get_streaming_platforms_no_results(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"results": {}}
    mocker.patch("src.api_client.requests.get", return_value=mock_response)

    result = get_streaming_platforms(99999, "ES")

    assert result["streaming"] == []
    assert result["rent"] == []
    assert result["buy"] == []
