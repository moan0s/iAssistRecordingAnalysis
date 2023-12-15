import argparse
import os
import tomli_w
import toml

if __name__ == "__main__":

    subjects = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
    for idx, subject in enumerate(subjects):
        print(f"{idx}: {subject}")
    while True:
        try:
            subject_number = int(input("Which subject to rename?\n"))
            break
        except ValueError:
            print("Please provide a integer!")
    new_subject_name = input("What to rename to?\n")

    old_subject_name = subjects[subject_number]

    sessions = [d for d in os.listdir(f'{old_subject_name}') if os.path.isdir(os.path.join(f"{old_subject_name}", d))]
    for session in sessions:
        experiements = [d for d in os.listdir(f'{old_subject_name}/{session}') if
                    os.path.isdir(os.path.join(f"{old_subject_name}/{session}", d))]
        for experiment in experiements:
            print(f"Renaming {session}/{experiment}")
            # Load toml
            with open(f"{old_subject_name}/{session}/{experiment}/recording_metadata.toml", 'r') as f:
                old_metadata = toml.load(f)
            new_metadata = old_metadata
            new_metadata["settings"]['subject'] = new_subject_name
            with open(f"{old_subject_name}/{session}/{experiment}/recording_metadata.toml", mode="wb") as fp:
                tomli_w.dump(new_metadata, fp)

    os.rename(old_subject_name, new_subject_name)




