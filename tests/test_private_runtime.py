"""Offline tests using only temporary synthetic keys, dictionaries and databases."""

import importlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from cryptography.fernet import Fernet

import runtime_paths


security = importlib.import_module(
    "Functions.security" if runtime_paths.ENV_PREFIX == "API" else "functions.security"
)
PREFIX = runtime_paths.ENV_PREFIX


class PrivateRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.env = patch.dict(os.environ, {}, clear=True)
        self.env.start()
        self.temp = tempfile.TemporaryDirectory(dir=runtime_paths.PROJECT_ROOT.parent)
        self.root = Path(self.temp.name).resolve()
        security._dicionarios.cache_clear()

    def tearDown(self):
        security._dicionarios.cache_clear()
        self.temp.cleanup()
        self.env.stop()

    def configure_dictionaries(self, encrypted=None, decrypted=None):
        key = Fernet.generate_key()
        fernet = Fernet(key)
        files = {
            "KEY_FILE": key,
            "CRIPTO_FILE": fernet.encrypt(json.dumps(
                encrypted if encrypted is not None else {"a": "x", "b": "y"}
            ).encode()),
            "DESCRIPTO_FILE": fernet.encrypt(json.dumps(
                decrypted if decrypted is not None else {"x": "a", "y": "b"}
            ).encode()),
        }
        for suffix, content in files.items():
            file_path = self.root / suffix.lower()
            file_path.write_bytes(content)
            os.environ[f"{PREFIX}_{suffix}"] = str(file_path)

    def test_import_reads_no_private_files(self):
        with patch("pathlib.Path.read_bytes", side_effect=AssertionError("private read")), \
                patch("builtins.open", side_effect=AssertionError("private read")):
            importlib.reload(security)

    def test_missing_configuration_fails_before_read(self):
        with patch("pathlib.Path.read_bytes", side_effect=AssertionError("private read")):
            with self.assertRaisesRegex(RuntimeError, f"{PREFIX}_KEY_FILE"):
                security.criptografar("synthetic")

    def test_all_paths_validated_before_any_private_read(self):
        self.configure_dictionaries()
        del os.environ[f"{PREFIX}_DESCRIPTO_FILE"]
        with patch("pathlib.Path.read_bytes", side_effect=AssertionError("private read")):
            with self.assertRaisesRegex(RuntimeError, f"{PREFIX}_DESCRIPTO_FILE"):
                security.descriptografar("synthetic")

    def test_synthetic_round_trip_preserves_unknown_characters(self):
        self.configure_dictionaries()
        self.assertEqual("xy! 123", security.criptografar("ab! 123"))
        self.assertEqual("ab! 123", security.descriptografar("xy! 123"))

    def test_wrong_key_fails_with_generic_error(self):
        self.configure_dictionaries()
        Path(os.environ[f"{PREFIX}_KEY_FILE"]).write_bytes(Fernet.generate_key())
        with self.assertRaisesRegex(RuntimeError, "^Unable to load configured private dictionaries.$"):
            security.criptografar("ab")

    def test_invalid_dictionary_format_fails_closed(self):
        self.configure_dictionaries(encrypted=["not", "a", "dictionary"])
        with self.assertRaisesRegex(RuntimeError, "^Unable to load configured private dictionaries.$"):
            security.criptografar("ab")

    def test_checkout_key_rejected_before_read(self):
        directory = "Functions" if PREFIX == "API" else "functions"
        os.environ[f"{PREFIX}_KEY_FILE"] = str(
            runtime_paths.PROJECT_ROOT / directory / "key.key"
        )
        with patch("pathlib.Path.read_bytes", side_effect=AssertionError("private read")):
            with self.assertRaisesRegex(RuntimeError, "outside the checkout"):
                security.criptografar("synthetic")

    def test_relative_key_rejected(self):
        os.environ[f"{PREFIX}_KEY_FILE"] = "key.key"
        with self.assertRaisesRegex(RuntimeError, "absolute path"):
            security.criptografar("synthetic")

    def test_missing_private_file_rejected(self):
        os.environ[f"{PREFIX}_KEY_FILE"] = str(self.root / "missing")
        with self.assertRaisesRegex(RuntimeError, "existing private file"):
            security.criptografar("synthetic")

    def test_data_directory_required(self):
        with self.assertRaisesRegex(RuntimeError, f"{PREFIX}_DATA_DIR"):
            runtime_paths.data_file("database.db")

    def test_checkout_data_directory_rejected(self):
        os.environ[f"{PREFIX}_DATA_DIR"] = str(runtime_paths.PROJECT_ROOT / "Data")
        with self.assertRaisesRegex(RuntimeError, "outside the checkout"):
            runtime_paths.data_file("database.db")

    def test_data_path_stays_in_external_root(self):
        os.environ[f"{PREFIX}_DATA_DIR"] = str(self.root / "runtime")
        result = runtime_paths.data_file("Logs", "example.txt")
        self.assertEqual(self.root / "runtime" / "Logs" / "example.txt", result)
        self.assertTrue(result.parent.is_dir())
        with self.assertRaisesRegex(RuntimeError, "within the configured data directory"):
            runtime_paths.data_file("..", "escaped.txt")

    def test_ancestor_data_root_cannot_return_to_checkout(self):
        os.environ[f"{PREFIX}_DATA_DIR"] = str(runtime_paths.PROJECT_ROOT.parent)
        for parts in ((runtime_paths.PROJECT_ROOT.name,),
                      (runtime_paths.PROJECT_ROOT.name, "synthetic-only.txt")):
            with self.subTest(parts=parts), patch("pathlib.Path.mkdir") as mkdir:
                with self.assertRaisesRegex(RuntimeError, "outside the checkout"):
                    runtime_paths.data_file(*parts)
                mkdir.assert_not_called()

    def test_database_created_only_in_synthetic_external_directory(self):
        os.environ[f"{PREFIX}_DATA_DIR"] = str(self.root)
        module = importlib.import_module("Functions.database" if PREFIX == "API" else "database")
        try:
            expected = self.root / "Data" / "database.db" if PREFIX == "API" else self.root / "database.db"
            self.assertEqual(expected.as_posix(), module.engine.url.database)
            self.assertTrue(expected.is_file())
        finally:
            module.engine.dispose()

    def test_relative_data_directory_rejected(self):
        os.environ[f"{PREFIX}_DATA_DIR"] = "Data"
        with self.assertRaisesRegex(RuntimeError, "absolute path"):
            runtime_paths.data_file("database.db")

    def test_connector_writes_only_synthetic_external_files(self):
        self.configure_dictionaries()
        os.environ[f"{PREFIX}_DATA_DIR"] = str(self.root / "runtime")
        connector = importlib.import_module("functions.connect")
        response = unittest.mock.Mock()
        response.json.return_value = {
            "id": 1, "nome": "xy", "idade": 99, "cpf": "xy",
            "gmail": "xy", "ano": 1900,
        }
        with patch.object(connector.requests, "get", return_value=response) as request:
            result = connector.conectar_api("https://api-c783.onrender.com/Usuarios", 1)
        self.assertEqual("CONECTADO", result)
        request.assert_called_once()
        received = self.root / "runtime" / "recived" / "recived.txt"
        result_file = self.root / "runtime" / "result" / "result.txt"
        self.assertTrue(received.is_file())
        self.assertIn("NOME: ab", result_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
