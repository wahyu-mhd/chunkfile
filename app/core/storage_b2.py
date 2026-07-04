from botocore.exceptions import ClientError
import boto3

from app.config import settings


def create_b2_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.b2_endpoint_url,
        region_name=settings.b2_region,
        aws_access_key_id=settings.b2_key_id,
        aws_secret_access_key=settings.b2_application_key,
    )


class B2Storage:
    def __init__(self):
        self.client = create_b2_client()
        self.bucket = settings.b2_bucket

    def upload_bytes(
        self,
        object_key: str,
        data: bytes,
        content_type: str = "application/octet-stream",
    ) -> None:
        self.client.put_object(
            Bucket=self.bucket,
            Key=object_key,
            Body=data,
            ContentType=content_type,
        )

    def download_bytes(self, object_key: str) -> bytes:
        response = self.client.get_object(
            Bucket=self.bucket,
            Key=object_key,
        )

        return response["Body"].read()

    def delete_object(self, object_key: str) -> None:
        self.client.delete_object(
            Bucket=self.bucket,
            Key=object_key,
        )

    def object_exists(self, object_key: str) -> bool:
        try:
            self.client.head_object(
                Bucket=self.bucket,
                Key=object_key,
            )
            return True
        except ClientError as error:
            status_code = error.response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status_code == 404:
                return False

            raise