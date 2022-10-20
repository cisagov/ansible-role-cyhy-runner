"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


def test_packages(host):
    """Test that the appropriate packages were installed."""
    shared_packages = [
        "python3-daemon",
        "python3-docopt",
        "python3-lockfile",
        "python3-requests",
    ]
    debian_packages = [*shared_packages, "python3-yaml"]
    redhat_packages = [*shared_packages, "python3-pyyaml"]

    if host.system_info.distribution in ["debian", "kali", "ubuntu"]:
        for pkg in debian_packages:
            assert host.package(pkg).is_installed
    elif host.system_info.distribution in ["fedora"]:
        for pkg in redhat_packages:
            assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["cyhy-runner"])
def test_pip_packages(host, pkg):
    """Test that the pip packages were installed."""
    assert pkg in host.pip_package.get_packages(pip_path="pip3")


@pytest.mark.parametrize(
    "directory",
    [
        {"mode": "0o755", "path": "/var/cyhy/runner"},
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
