"""
Scrape app information from Google Play Store
"""

import os
import csv
import time
import concurrent.futures

from scraper import get_app_info


start = time.time()


def get_desktop():
    """Absolute path to Desktop of the user based on the OS."""
    if os.name == "nt":
        return os.path.expanduser("~\\Desktop")  # Windows
    else:
        return os.path.expanduser("~/Desktop")  # Linux & Mac


def get_input_app_data():
    """Search and return the name of a CSV file containing data of 50k apps."""
    for root_dir, sub_dirs, files in os.walk(os.getcwd()):
        for filename in files:
            if filename.endswith(".csv"):
                return filename
    return None


def get_app_details(row):
    """Return detailed app information with the given app id."""
    app_id = row[1]
    app_info = get_app_info(app_id)

    if app_info is not None:
        app_detail = row[:-1] + [app_info["icon"]] + row[-1:]
        return app_detail
    else:
        return None


def save_to_csv(row):
    """Save updated Google Play data to CSV."""

    headers = (
        "App Name,App Id,Category,Rating,Rating Count,Installs,"
        "Minimum Installs,Maximum Installs,Free,Price,Currency,Size,"
        "Minimum Android,Developer Id,Developer Website,Developer Email,"
        "Released,Last Updated,Content Rating,Privacy Policy,Ad Supported,"
        "In App Purchases,Editors Choice,Icon URL,Scraped Time"
    )

    if row is not None:
        filename = "Google-Play-Updated.csv"
        output_path = os.path.join(get_desktop(), filename)

        mode = "a" if os.path.exists(output_path) else "w"
        with open(output_path, mode=mode, encoding="utf=8", newline="") as f:
            csv_writer = csv.writer(f)
            if mode == "w":
                csv_writer.writerow(headers.split(","))

            csv_writer.writerow(row)


input_app_data = get_input_app_data()

if input_app_data is not None:

    with open(input_app_data, encoding="utf-8") as f:
        csv_reader = csv.reader(f)
        next(csv_reader)  # skip the header

        print("Extracting app info...")
        try:
            # # Sequential extraction of app info
            # for row in csv_reader:
            #     app_id = row[1]
            #     app_info = get_app_info(app_id)
            #     app_detail = row[:-1] + [app_info["icon"]] + row[-1:]
            #     save_to_csv(app_detail)

            # use multi-threading to speed up scraping
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                future = {
                    executor.submit(get_app_details, row): row for row in csv_reader
                }
                for future in concurrent.futures.as_completed(future):
                    try:
                        app_detail = future.result()
                    except Exception as e:
                        print("Error occurred: ", e.with_traceback())
                    else:
                        save_to_csv(app_detail)

            print("Finished scraping:\n")
            print(
                'Output data saved in Desktop with filename: "Google-Play-Updated.csv"'
            )

        except Exception as e:
            print("Error occured: ", e.with_traceback())

    end = time.time()
    print("Time taken: ", end - start, " seconds.")
else:
    print("Error: a CSV file containing app data not found.\n")
    print("Have you copied it to current folder?")
