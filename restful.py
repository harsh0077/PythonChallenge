import argparse
import requests
import json
import csv

class RestfulClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self):
        self.parser = self.create_arg_parser()

    def create_arg_parser(self):
        parser = argparse.ArgumentParser(description="Simple command-line REST client for JSONPlaceholder.")
        parser.add_argument("method", choices=["get", "post"], help="HTTP method (get or post).")
        parser.add_argument("endpoint", help="URI fragment (e.g., /posts/1).")
        parser.add_argument("-o", "--output", help="Output file (JSON or CSV).")
        parser.add_argument("--title", help="Title for POST request.")
        parser.add_argument("--body", help="Body for POST request.")
        parser.add_argument("--user-id", type=int, help="User ID for POST request.")
        return parser

    def run(self):
        args = self.parser.parse_args()
        method = args.method.lower()
        endpoint = args.endpoint

        if method == "get":
            response = requests.get(f"{self.BASE_URL}{endpoint}")
        elif method == "post":
            data = {"title": args.title, "body": args.body, "userId": args.user_id}
            response = requests.post(f"{self.BASE_URL}{endpoint}", json=data)

        self.handle_response(response, args.output)

    def handle_response(self, response, output_file):
        print(f"HTTP Status Code: {response.status_code}")

        if response.ok:
            if output_file:
                if output_file.endswith(".json"):
                    self.save_to_json(response.json(), output_file)
                elif output_file.endswith(".csv"):
                    self.save_to_csv(response.json(), output_file)
                else:
                    print("Unsupported output format. Supported formats: .json, .csv")
            else:
                print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.text}")

    @staticmethod
    def save_to_json(data, filename):
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=2)
        print(f"Response saved to {filename}")

    @staticmethod
    def save_to_csv(data, filename):
        if isinstance(data, list) and data:
            keys = data[0].keys()
            with open(filename, 'w', newline='') as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=keys)
                writer.writeheader()
                writer.writerows(data)
            print(f"Response saved to {filename}")
        else:
            print("Invalid data format for CSV export.")

if __name__ == "__main__":
    client = RestfulClient()
    client.run()
