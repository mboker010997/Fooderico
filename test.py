import os
import subprocess
import unittest


class TestCodeStyle(unittest.TestCase):
    def test_flake8_conformance(self):
        project_dir = '.'

        python_files = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('.py'):
                    python_files.append(os.path.join(root, file))

        all_errors = []
        for python_file in python_files:
            result = subprocess.run(['flake8', python_file],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                all_errors.append(
                    f'Файл {python_file} не соответствует '
                    f'стандарту Flake8:\n{result.stdout}'
                )

        if all_errors:
            self.fail('\n'.join(all_errors))


if __name__ == '__main__':
    unittest.main()
