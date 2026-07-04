from core.paths import paths


def test_project_root_exists():
    assert paths.project_root.exists()


def test_src_exists():
    assert paths.src.exists()


def test_initialize():

    paths.initialize()

    assert paths.data.exists()
    assert paths.database.exists()
    assert paths.logs.exists()
    assert paths.uploads.exists()
    assert paths.output.exists()
    assert paths.backups.exists()