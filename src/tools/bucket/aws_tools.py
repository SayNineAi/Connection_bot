import boto3
import os
from botocore.exceptions import ClientError


class AWSTools:
    def __init__(self):
        self.BUCKET_NAME = "linkedin-bot-bucket"
        self.LOCAL_DATA_FOLDER = "data/input/"
        self.init_s3()

    def init_s3(self):
        self.s3 = boto3.client("s3")

    def upload_output_to_s3(self, filename):
        try:
            resp = self.s3.upload_file(
                filename, self.BUCKET_NAME, "outputs/{}".format(filename.split("/")[-1])
            )
        except ClientError as e:
            print(e)

    def upload_all_outputs(self, dir):
        files = os.listdir(dir)
        print("Files: ", files)
        for filename in files:
            print("File: ", filename)
            self.upload_output_to_s3(dir + filename)

    def get_input_from_bucket(self, username, ext):
        self.s3.download_file(
            self.BUCKET_NAME,
            "inputs/{}_input.{}".format(username, ext),
            "{}/{}".format(self.LOCAL_DATA_FOLDER, "{}_input.{}".format(username, ext)),
        )
