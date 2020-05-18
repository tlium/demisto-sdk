import os

import pytest
from demisto_sdk.commands.common.git_tools import git_path
from demisto_sdk.commands.common.hook_validations.release_notes import \
    ReleaseNotesValidator


def get_validator(file_path='', modified_files=None):
    release_notes_validator = ReleaseNotesValidator("")
    release_notes_validator.file_path = file_path
    release_notes_validator.release_notes_path = file_path
    release_notes_validator.latest_release_notes = file_path
    release_notes_validator.modified_files = modified_files
    return release_notes_validator


FILES_PATH = os.path.normpath(os.path.join(__file__, f'{git_path()}/demisto_sdk/tests', 'test_files'))
nothing_in_rn = ''
rn_not_filled_out = '%%UPDATE_RN%%'
rn_filled_out = 'This are sample release notes'
diff_package = [(nothing_in_rn, False),
                (rn_not_filled_out, False),
                (rn_filled_out, True)]


class RNValidationTest:
    @pytest.mark.parametrize('release_notes, expected_result', diff_package)
    def test_rn_master_diff(self, release_notes, expected_result, mocker):
        """
        Given
        - Case 1: Empty release notes.
        - Case 2: Not filled out release notes.
        - Case 3: Valid release notes

        When
        - Running validation on release notes.

        Then
        - Ensure validation correctly identifies valid release notes.
        - Case 1: Should return the prompt "Please complete the release notes found at: {path}" and
                  return False
        - Case 2: Should return the prompt "Please finish filling out the release notes found at: {path}" and
                  return False
        - Case 3: Should print nothing and return True
        """
        mocker.patch.object(ReleaseNotesValidator, '__init__', lambda a, b: None)
        validator = get_validator(release_notes)
        assert validator.is_file_valid() == expected_result
        assert 1 == 2

    @staticmethod
    def test_init():
        """
        Given
        - Release notes file path

        When
        - Running validation on release notes.

        Then
        - Ensure init returns valid file path and release notes contents.
        """
        filepath = os.path.join(FILES_PATH, 'ReleaseNotes', '1_1_1.md')
        release_notes_validator = ReleaseNotesValidator(filepath)
        release_notes_validator.file_path = 'demisto_sdk/tests/test_files/ReleaseNotes/1_1_1.md'
        assert release_notes_validator.release_notes_path == filepath
        assert release_notes_validator.latest_release_notes == '### Test'

    TEST_RELEASE_NOTES_TEST_BANK = [
        ('', False),  # Completely Empty
        ('#### Integrations\n- __HelloWorld__\n  - Grammar correction for code '  # Missing Items
         'description.\n\n#### Scripts\n- __HelloWorldScript__\n  - Grammar correction for '
         'code description. ', False)
    ]
    MODIFIED_FILES = [
        'Packs/HelloWorld/Integrations/HelloWorld/HelloWorld.py',
        'Packs/HelloWorld/IncidentTypes/incidenttype-Hello_World_Alert.json',
        'Packs/HelloWorld/IncidentFields/incidentfield-Hello_World_ID.json',
        'Packs/HelloWorld/Layouts/layout-details-Hello_World_Alert-V2.json'
    ]

    @pytest.mark.parametrize('release_notes, expected_result', TEST_RELEASE_NOTES_TEST_BANK)
    def test_are_release_notes_complete(self, release_notes, expected_result, mocker):
        """
        Given
        - Case 1: Empty release notes.
        - Case 2: Not filled out release notes.
        - Case 3: Valid release notes

        When
        - Running validation on release notes.

        Then
        - Ensure validation correctly identifies valid release notes.
        - Case 1: Should return the prompt "Please complete the release notes found at: {path}" and
                  return False
        - Case 2: Should return the prompt "Please finish filling out the release notes found at: {path}" and
                  return False
        - Case 3: Should print nothing and return True
        """
        mocker.patch.object(ReleaseNotesValidator, '__init__', lambda a, b: None)
        validator = get_validator(release_notes, self.MODIFIED_FILES)
        assert validator.are_release_notes_complete() == expected_result
