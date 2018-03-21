$PROJECT = 'lazyasd'
$ACTIVITIES = ['version_bump', 'changelog', 'tag', 'push_tag', 'pypi', 'conda_forge', 'ghrelease']

$VERSION_BUMP_PATTERNS = [
    ('lazyasd-py2.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('lazyasd-py3.py', '__version__\s*=.*', "__version__ = '$VERSION'"),
    ('setup.py', 'VERSION\s*=.*', "VERSION = '$VERSION'")
    ]
$CHANGELOG_FILENAME = 'CHANGELOG.rst'
$CHANGELOG_IGNORE = ['TEMPLATE.rst']
$PUSH_TAG_REMOTE = 'git@github.com:xonsh/lazyasd.git'

$GITHUB_ORG = 'xonsh'
$GITHUB_REPO = 'lazyasd'
