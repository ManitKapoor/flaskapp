import boto3

client = boto3.client('dynamodb', region_name='us-east-1')

def add_records():
    BooksTable = boto3.resource('dynamodb').Table('Books')
    with BooksTable.batch_writer() as batch:
        batch.put_item(Item={"Author": "Manit Kapoor", "Title": "The CodeMaker",
                             "Category": "Suspense", "Link": "http://Link1.com"})
        batch.put_item(Item={"Author": "Madan Kapoor", "Title": "The CodeMaker 2",
                             "Category": "Suspense", "Link": "http://Link2.com"})
        batch.put_item(Item={"Author": "Jack Drew", "Title": "No Love",
                             "Category": "Romance", "Link": "http://Link3.com"})


def create_table():
    try:
        resp = client.create_table(
            TableName="Books",
            KeySchema=[
                {
                    "AttributeName": "Title",
                    "KeyType": "HASH"
                }, {
                    "AttributeName": "Author",
                    "KeyType": "RANGE"
                }
            ],
            AttributeDefinitions=[
                {
                    "AttributeName": "Title",
                    "AttributeType": "S"
                }, {
                    "AttributeName": "Category",
                    "AttributeType": "S"
                }, {
                    "AttributeName": "Name",
                    "AttributeType": "S"
                }, {
                    "AttributeName": "Author",
                    "AttributeType": "S"
                }
            ],
            ProvisionedThroughput={
                "ReadCapacityUnits": 1,
                "WriteCapacityUnits": 1
            },
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'CategoryIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'Category',
                            'KeyType': 'HASH'
                        }, {
                            "AttributeName": "Name",
                            "KeyType": "RANGE"
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    },
                    'ProvisionedThroughput': {
                        'ReadCapacityUnits': 1,
                        'WriteCapacityUnits': 1
                    }
                }
            ]
        )
        print("Table created successfully!")
    except Exception as e:
        print("Error creating table:")
        print(e)

table_name = "Books"
existing_tables = client.list_tables()['TableNames']
if table_name not in existing_tables:
    create_table()
add_records()