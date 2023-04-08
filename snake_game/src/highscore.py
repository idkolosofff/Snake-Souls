class Highscore:
    def __init__(self, file_name="personal_records.txt"):
        self.file_name = file_name
        self.records = self.load_personal_records()

    def load_personal_records(self):
        try:
            with open(self.file_name, "r") as file:
                records = [int(line.strip()) for line in file.readlines()]
        except FileNotFoundError:
            records = []

        return sorted(records, reverse=True)

    def save_personal_records(self):
        with open(self.file_name, "w") as file:
            for record in self.records:
                file.write(f"{record}\n")

    def add_record(self, new_record):
        self.records.append(new_record)
        self.records.sort(reverse=True)

        # Keep only the top 10 records
        if len(self.records) > 10:
            self.records.pop()

        self.save_personal_records()

    def get_personal_records(self):
        return self.records

