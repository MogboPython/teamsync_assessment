# TeamSync Assessment
This project holds the code for my submission for the assessment project given to me by TeamSync.


## Setting up locally

To setup the project locally clone the repository.

```shell
git clone https://github.com/MogboPython/teamsync_assessment.git
```

Install required dependencies.

```shell
pip install -r requirements.txt
```

To run the server in development mode. The `--reload` tells the server to run in debug mode.

```shell
uvicorn main:app --reload
```

To see the routes go to the following in your browser.

```
127.0.0.1:8000/docs
```

## For the live deployment.
```
https://teamsync.fly.dev/docs
```