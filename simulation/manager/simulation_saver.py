from pathlib import Path
import json
from filelock import SoftFileLock, Timeout


class SimulationSaver:

    def __init__(
        self, filename: str, simulation_dict: dict, simulation_parameter: float = None
    ):
        self.simulation_parameter = str(simulation_parameter)
        self.write_file = f"./data/{filename}"
        self.simulation_dict = simulation_dict
        self.using_simulation_parameter = simulation_parameter is not None

    def save(self) -> None:
        """Save the file to ./data/filename, wait for file lock."""
        lock = SoftFileLock(f"{self.write_file}.lock", timeout=180)
        with lock:
            if Path(self.write_file).is_file():
                self._save_existing()
            else:
                self._save_new()

    def _save_existing(self) -> None:
        # Check if the existing file is using a simulation parameter or not
        with open(self.write_file, "r") as outfile:
            file_data = json.load(outfile)
            file_using_simulation_parameter = file_data["simulation_parameter"]
            if self.using_simulation_parameter != file_using_simulation_parameter:
                self._save_new()
                return

        # We are now certain that our file format matches the format we have
        # Update values
        if self.using_simulation_parameter:
            # Check if there is a simulation parameter value that matches the current one
            if self.simulation_parameter in file_data:
                run_number_strings = list(file_data[self.simulation_parameter].keys())
                run_numbers = [int(i) for i in run_number_strings]
                key_offset = max(run_numbers) + 1
                self._update_simulation_dict_keys(key_offset)
                file_data[self.simulation_parameter].update(self.simulation_dict)
            else:
                file_data[self.simulation_parameter] = self.simulation_dict
        else:
            run_number_strings = list(file_data.keys())
            run_number_strings.remove("simulation_parameter")
            run_numbers = [int(i) for i in run_number_strings]
            key_offset = max(run_numbers) + 1
            self._update_simulation_dict_keys(key_offset)
            file_data.update(self.simulation_dict)

        with open(self.write_file, "w") as outfile:
            json.dump(file_data, outfile)

    def _save_new(self) -> None:
        with open(self.write_file, "w") as outfile:
            if self.using_simulation_parameter:
                temp_simulation_dict = self.simulation_dict
                self.simulation_dict = {}
                self.simulation_dict[self.simulation_parameter] = temp_simulation_dict
                self.simulation_dict["simulation_parameter"] = True
            else:
                self.simulation_dict["simulation_parameter"] = False

            json.dump(self.simulation_dict, outfile)

    def _update_simulation_dict_keys(self, key_offset):
        self.simulation_dict = {
            (run_number + key_offset): run_data
            for run_number, run_data in self.simulation_dict.items()
        }
