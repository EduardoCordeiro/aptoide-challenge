#### Running the application
1. Create a virtul env, install poetry (1.4.2) and then run poetry install (This app was built on python 3.11)
2. Run `uvicorn main:app` to start the server
3. In a new terminal window run the client: `python client.py {app} {product} {user}`

##### Assumptions:
1. Each item can only belong to one store
2. Each item has unlimited quantity
3. Took some liberties with the output format, for example ignoring the euro sign in some cases

##### Running the tests

I only created a couple tests, but I think they are good examples of how to test this application.

1. `python -m pytest .`
