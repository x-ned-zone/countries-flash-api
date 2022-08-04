Web service REST API:

Request ->  
    REST Controller -> 
        REST API Service layer -> 
            Repository db ->  
                Response

Have not mocked the app on the test class, so the App needs to be launched before unit test cases.

Tests should all pass on a clean slate of Database. Local database should be empty or deleted.
Delete is soft delete; For now I have not implemented a way to pass additional parameters to the delete REST method when testing to allow hard deleting.
