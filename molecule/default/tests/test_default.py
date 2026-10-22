"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize("pkg_name,pkg_version", [("cyhy-runner", "3.0.1")])
def test_pip_packages(host, pkg_name, pkg_version):
    """Test that the pip packages were installed."""
    pip_packages = host.pip.get_packages(pip_path="/usr/bin/pip3")

    assert pkg_name in pip_packages
    assert pip_packages[pkg_name]["version"] == pkg_version


@pytest.mark.parametrize(
    "directory",
    [
        {"mode": "0o755", "path": "/var/cyhy/runner"},
        {"mode": "0o755", "path": "/var/cyhy/runner/done"},
        {"mode": "0o755", "path": "/var/cyhy/runner/running"},
        {"mode": "0o755", "path": "/var/log/cyhy"},
    ],
)
def test_directories(host, directory):
    """Test that the appropriate directories were created."""
    assert host.file(directory["path"]).exists
    assert host.file(directory["path"]).is_directory
    assert oct(host.file(directory["path"]).mode) == directory["mode"]


@pytest.mark.parametrize(
    "file",
    [
        {"mode": "0o644", "path": "/lib/systemd/system/cyhy-runner.service"},
    ],
)
def test_files(host, file):
    """Test that the expected files are present."""
    assert host.file(file["path"]).exists
    assert host.file(file["path"]).is_file
    assert oct(host.file(file["path"]).mode) == file["mode"]


@pytest.mark.parametrize("svc", ["cyhy-runner"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled
