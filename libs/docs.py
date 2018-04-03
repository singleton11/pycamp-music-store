import os
import re

import markdown


def get_container_start_time(
    file_path='./docs_build/index.html',
    pattern='^build\sdate\s.*\:\s([0-9\:\s\-]*)'
):
    """Get container start time by regular expression template `pattern`
    from `file_path` file

    Used in `main_page.py` to display when docker container was ran.

    Args:
        file_path(str) - path of file which contains required timestamped info
        pattern(str) - regular expression pattern which define format of
                       searched string with timestamp

    At the end of `docs_build/index.html` we can find the time when this docs
    files were built. And we can use this time as docker container start time

    Return:
        str - string representation of timestamped value
    """
    build_date = ''

    if not os.path.exists(file_path):
        return ''

    with open(file_path) as f:

        # iterate through file lines from end to start
        for line in reversed(f.readlines()):
            result = re.match(pattern, line, flags=re.IGNORECASE)
            if result:
                build_date = result.group(0)
                break

    return build_date


def get_changelog_preview(changelog_path, version_amount):
    """This function is helper which returns last changes from changelog

    Args:
        changelog_path(str) - os path to changelog file
        version_amount(int) - how many items(versions) should preview include

    `version_amount` is amount of items from changelog file such as:

        # ?.?.? - <version number>

        <Description of changes which were made for single task>


    Return:
        str - html string which generated from markdown
    """
    changelog_lines = []
    if not os.path.exists(changelog_path):
        return ''

    with open(changelog_path) as f:
        for line in f:
            if re.match('^#\s(\d+)\.(\d+)\.(\d+)$', line):
                version_amount -= 1

            if version_amount <= 0:
                break

            changelog_lines.append(line)

    if not changelog_lines:
        return ''

    # exclude first and second strings (changelog title and blank line)
    changelog_preview = '\n'.join(changelog_lines[2:])

    # make html from markdown
    changelog_preview = markdown.markdown(changelog_preview)

    return changelog_preview
