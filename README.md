# my-fastapi-rest-api
This is a REST API built with FastAPI. It follows a modular architecture with separate layers for Controllers, DTOs, DAOs, Routes, Models Exceptions, and Configurations. The API includes endpoints for transcribe audio, video and chat with content storage in DB from this files and media resources.

## Installation
0. From the command line or console, create a Python environment using the command "python -m venv name_environment"
1. Clone the repository of project, move to root path of environment and active it with line ".\name_environment\Scripts\activate". Then move to root path of project.
2. Install the dependencies listed in `requirements.txt` with "pip install -r requirements.txt". This step can to take some minutes, depends on your internet speed.
3. Install ffmpeg, for example see the video https://www.youtube.com/watch?v=0zN9oZ98ZgE to see how install it in windows.
4. Edit the `config.py` file to set the correct paths for the models and the database.
5. Run the `app.py` file to start the API. The first time can to take several minutes for donwload small and medium whisper models. The command for run is "uvicorn app:app --reload".

## Usage

-Undocumented as of the current date.

## License

-Undocumented as of the current date.