# SPDX-License-Identifier: GPL-3.0-or-later
#
# This file is part of Nominatim. (https://nominatim.org)
#
# Copyright (C) 2025 by the Nominatim developer community.
# For a full list of authors see the git log.
"""
Test for the command line interface wrapper admin subcommand.

These tests just check that the various command line parameters route to the
correct functionality. They use a lot of monkeypatching to avoid executing
the actual functions.
"""
import pytest

import nominatim_db.tools.admin
import nominatim_db.tools.check_database
import nominatim_db.tools.migration
import nominatim_db.clicmd.admin


def test_admin_command_check_database(cli_call, mock_func_factory):
    mock = mock_func_factory(nominatim_db.tools.check_database, 'check_database')

    assert cli_call('admin', '--check-database') == 0
    assert mock.called == 1


def test_admin_migrate(cli_call, mock_func_factory):
    mock = mock_func_factory(nominatim_db.tools.migration, 'migrate')

    assert cli_call('admin', '--migrate') == 0
    assert mock.called == 1


def test_admin_clean_deleted_relations(cli_call, mock_func_factory):
    mock = mock_func_factory(nominatim_db.tools.admin, 'clean_deleted_relations')

    assert cli_call('admin', '--clean-deleted', '1 month') == 0
    assert mock.called == 1


def test_admin_clean_deleted_relations_no_age(cli_call, mock_func_factory):
    mock_func_factory(nominatim_db.tools.admin, 'clean_deleted_relations')

    assert cli_call('admin', '--clean-deleted') == 1


class TestCliAdminWithDb:

    @pytest.fixture(autouse=True)
    def setup_cli_call(self, cli_call, temp_db, cli_tokenizer_mock):
        self.call_nominatim = cli_call
        self.tokenizer_mock = cli_tokenizer_mock

    @pytest.mark.parametrize("func, params", [('analyse_indexing', ('--analyse-indexing', ))])
    def test_analyse_indexing(self, mock_func_factory, func, params):
        mock = mock_func_factory(nominatim_db.tools.admin, func)

        assert self.call_nominatim('admin', *params) == 0
        assert mock.called == 1
