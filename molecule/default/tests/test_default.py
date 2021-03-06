"""Module containing the tests for the default scenario."""

# Standard Python Libraries
import os

# Third-Party Libraries
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ["MOLECULE_INVENTORY_FILE"]
).get_hosts("all")


@pytest.mark.parametrize(
    "pkg", ["python3-daemon", "python3-docopt", "python3-lockfile", "python3-requests"]
)
def test_packages(host, pkg):
    """Test that the appropriate packages were installed."""
    assert host.package(pkg).is_installed


@pytest.mark.parametrize("pkg", ["cyhy-runner"])
def test_pip_packages(host, pkg):
    """Test that the pip packages were installed."""
    assert pkg in host.pip_package.get_packages(pip_path="pip3")


@pytest.mark.parametrize(
    "f",
    [
        "/var/log/cyhy",
        "/lib/systemd/system/cyhy-runner.service",
    ],
)
def test_files(host, f):
    """Test that the expected files and directories are present."""
    assert host.file(f).exists


@pytest.mark.parametrize("svc", ["cyhy-runner"])
def test_services(host, svc):
    """Test that the services were enabled."""
    assert host.service(svc).is_enabled
