import os
import subprocess
import unittest


class TestCodeStyle(unittest.TestCase):
    def test_flake8_conformance(self):
        project_dir = '/src'

        python_files = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('py') and file != '__init__.py':
                    python_files.append(os.path.join(root, file))

        all_errors = []
        for python_file in python_files:
            result = subprocess.run(['flake8', '--max-line-length', '124', '--ignore=F403', python_file],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                error_message = (
                    f'File {python_file} does not conform '
                    f'to the Flake8 standard:\n{result.stdout}'
                )
                all_errors.append(error_message)

        self.assertEqual(len(all_errors), 0, '\n'.join(all_errors))


if __name__ == '__main__':
    unittest.main()
