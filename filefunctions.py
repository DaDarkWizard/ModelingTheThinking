

class file_handler:
    # Open the file
    def __init__(self, toOpen : str):
        self.file = open(toOpen, 'r+')
        if self.file < 0:
            return -1

    def get_file(self):
        # Returns file object
        return self.file

    def save_file(self):
        # Parse updates to CML form
        # Write back to file
        None
