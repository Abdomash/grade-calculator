import sys
import io
import re
import pydoc

class Pager:
    ANSI_ESCAPE_PATTERN = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def __init__(self):
        self.original_stdout = sys.stdout
        self.output_capture = io.StringIO()
        self.captured_content = ''
        self.capture_output_stream()
    
    def __enter__(self):
        self.capture_output_stream()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.capture_output()
        self.reset_output_stream()
        self.view_captured_content()

    def capture_output_stream(self):
        sys.stdout = self.output_capture

    def capture_output(self):
        self.captured_content = self.output_capture.getvalue()

    def reset_output_stream(self):
        sys.stdout = self.original_stdout

    def view_captured_content(self):
        self.capture_output()
        self.reset_output_stream()
        stripped_content = self.ANSI_ESCAPE_PATTERN.sub('', self.captured_content)
        pydoc.pager(stripped_content)