"""Tests for the parameter files shipped in openeo_udp/params/."""

from pathlib import Path

import pytest

from openeo_udp import ParameterManager, list_parameter_files

PACKAGED_FILES = list_parameter_files()

LOCAL_PARAMS = """
from openeo.api.process import Parameter


def get_parameters():
    return {
        "local_set": {
            "location_name": "Local override",
            "bounding_box": Parameter("bounding_box", default={"west": 0, "south": 0, "east": 1, "north": 1}),
        }
    }
"""


def test_params_files_are_packaged():
    assert "urban_areas.params.py" in PACKAGED_FILES
    assert len(PACKAGED_FILES) == len(set(PACKAGED_FILES))


# Self-contained notebook folders whose parameter files intentionally stay next
# to the notebook and are not shipped with the openeo_udp package.
STANDALONE_NOTEBOOK_DIRS = {
    Path("notebooks/sentinel/sentinel-2/forest_fire_dNBR"),
    Path("notebooks/sentinel/sentinel-2/burned_forest_classification_ml"),
}


def test_no_params_files_left_in_notebooks():
    repo_root = Path(__file__).resolve().parents[1]
    leftovers = sorted(
        path.relative_to(repo_root)
        for path in repo_root.glob("notebooks/**/*.params.py")
        if not any(
            path.relative_to(repo_root).is_relative_to(d)
            for d in STANDALONE_NOTEBOOK_DIRS
        )
    )
    assert leftovers == [], f"Move these into openeo_udp/params/: {leftovers}"


def test_standalone_params_files_are_not_packaged():
    repo_root = Path(__file__).resolve().parents[1]
    for d in STANDALONE_NOTEBOOK_DIRS:
        for path in (repo_root / d).glob("*.params.py"):
            assert path.name not in PACKAGED_FILES


@pytest.mark.parametrize("file_name", PACKAGED_FILES)
def test_packaged_params_file_loads(file_name, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # No local file with this name
    manager = ParameterManager(file_name)
    assert manager.param_file.name == file_name
    assert "openeo_udp" in manager.param_file.parts
    assert manager.list_parameter_sets()


def test_local_file_takes_precedence(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "urban_areas.params.py").write_text(LOCAL_PARAMS)
    manager = ParameterManager("urban_areas.params.py")
    assert manager.list_parameter_sets() == ["local_set"]


def test_missing_bare_name_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(FileNotFoundError):
        ParameterManager("does_not_exist.params.py")


def test_path_with_directory_does_not_fall_back(tmp_path):
    with pytest.raises(FileNotFoundError):
        ParameterManager(tmp_path / "missing" / "urban_areas.params.py")


def test_describe_source_packaged(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    manager = ParameterManager("urban_areas.params.py")
    assert manager.is_packaged
    assert manager.describe_source() == "urban_areas.params.py (packaged with openeo-udp)"


def test_describe_source_warns_when_local_overrides_packaged(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "urban_areas.params.py").write_text(LOCAL_PARAMS)
    manager = ParameterManager("urban_areas.params.py")
    assert not manager.is_packaged
    assert "(local file)" in manager.describe_source()
    assert "overrides the packaged" in manager.describe_source()


def test_describe_source_local_only_has_no_warning(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "my_algorithm.params.py").write_text(LOCAL_PARAMS)
    manager = ParameterManager("my_algorithm.params.py")
    assert "(local file)" in manager.describe_source()
    assert "overrides" not in manager.describe_source()


def test_print_options_shows_parameter_file(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    ParameterManager("urban_areas.params.py").print_options("urban areas")
    assert "Parameter file: urban_areas.params.py (packaged with openeo-udp)" in capsys.readouterr().out
