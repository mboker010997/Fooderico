import os
import subprocess
import unittest


class TestCodeStyle(unittest.TestCase):
    def test_flake8_conformance(self):
        project_dir = '/src'
        # project_dir = '/home/alexey/prac/tele-meet-bot/src/bot'

        python_files = []
        for root, dirs, files in os.walk(project_dir):
            for file in files:
                if file.endswith('py') and file != '__init__.py':
                    python_files.append(os.path.join(root, file))

        all_errors = []
        for python_file in python_files:
            result = subprocess.run(['flake8', python_file],
                                    capture_output=True, text=True)
            if result.returncode != 0:
                error_message = (
                    f'Файл {python_file} не соответствует '
                    f'стандарту Flake8:\n{result.stdout}'
                )
                print(error_message)
                all_errors.append(error_message)

        self.assertEqual(len(all_errors), 0, '\n'.join(all_errors))


if __name__ == '__main__':
    unittest.main()
