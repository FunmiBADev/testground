import pytest
import pandas as pd
from unittest.mock import patch


@pytest.fixture
def mock_get_password():
    with patch("your_script.get_password") as mock_get_password:
        mock_get_password.return_value = "platform_password"
        yield mock_get_password


@pytest.fixture
def mock_get_platform_token():
    with patch("your_script.get_platform_token") as mock_get_platform_token:
        mock_get_platform_token.return_value = "platform_token"
        yield mock_get_platform_token


@pytest.fixture
def mock_requests_get(mocker):
    mock_response = mocker.Mock()
    mock_response.json.return_value = [
        {
            "assemblies": ["assembly1", "assembly2"],
            "variables": [{"key": "VAR1", "value": "value1"}],
            "startCmd": "java -jar some.jar",
            "name": "process1",
            "host": "host1",
        },
        {
            "assemblies": ["assembly3"],
            "variables": [],
            "startCmd": "",
            "name": "process2",
            "host": "host2",
        },
    ]
    with patch("requests.get") as mock_get:
        mock_get.return_value = mock_response
        yield mock_get


def test_fetch_and_update_data(mock_get_password, mock_get_platform_token, mock_requests_get):
    # Mock data
    platform_tags = [{"url": "platform_url", "tag": "platform_tag"}]
    username = "username"

    # Call the function
    fetch_and_update_data(platform_tags, username)

    # Assertions
    assert len(combined_df) == 2
    assert combined_df.iloc[0]["name"] == "process1"
    assert combined_df.iloc[0]["host"] == "host1"
    assert combined_df.iloc[0]["jre"] == "jre_version_from_find_jre"
    assert combined_df.iloc[0]["jre_version"] == "parsed_jre_version"
    assert combined_df.iloc[0]["platform_tag"] == "platform_tag"
    assert combined_df.iloc[0]["green_jres"] is None
    assert combined_df.iloc[0]["eol_jres"] == "parsed_jre_version" if "1.8.0" in "parsed_jre_version" else None
    assert combined_df.iloc[0]["env_var_cmd"] == "parsed_jre_version" if "JAVA 8" in "parsed_jre_version" else None
    assert combined_df.iloc[1]["name"] == "process2"
    assert combined_df.iloc[1]["host"] == "host2"
    assert pd.isna(combined_df.iloc[1]["jre"])
    assert pd.isna(combined_df.iloc[1]["jre_version"])
    assert combined_df.iloc[1]["platform_tag"] == "platform_tag"
    assert combined_df.iloc[1]["green_jres"] is None
    assert combined_df.iloc[1]["eol_jres"] is None
    assert combined_df.iloc[1]["env_var_cmd"] is None

    # Mock calls
    mock_get_password.assert_called_once_with("platform_tag")
    mock_get_platform_token.assert_called_once_with("platform_url", username, "platform_password")
    mock_requests_get.assert_called_once_with(f"platform_url{PLATFORM_API_PROCESS_DEFINITIONS}", headers={"Cookie": "platform_token"})
