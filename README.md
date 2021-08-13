# Project

## Project Structure

- `app` folder: for code related to running the app

  - `api.py` : url and logic for api requests to be made
  - `config.py` : To contain the configuration of some of the critical variables
  - `database.py` : Codes to manipulate the database
  - `login.py` : Login logic and url to login
  - `vars.py` : Some useful variables that might need to be used.
  - `views.py` : To view the page. Avoid processing data here.

  <br>

  - `static` folder: for scripts, css and images for any html page.

    - `styles.css` for all the styling.

    - `scripts` folder: for any js scripts
      - `script.js`: for any general purpose js across multiple pages
      - `summary.js`: vue code for the summary page
    - `assets` folder: for images, fonts etc
      - `images` folder: for images

  - `templates` folder: for all the different html pages for Flask to render

  `utilities` folder:

  - `database_update.py`: utility for updating/setting up the database

<br>

- `requirements.txt`: the packages and version that is used.  
  Use `pip freeze` to generate it when in a virtual environment.

### Misc

- To run the flask code, run the `run.py` file.
- Create any other files needed to improve the structure.
- Schema (database, api, css class): https://docs.google.com/document/d/1cnTBuBVuUCJdrRCjcoP0eZie31BGKTb4XK3g6L5Tw-s/edit?usp=sharing

## Heroku

- Go to http://nysecure.herokuapp.com/ to view the app.
- Add environment variables there.  
  **Used for sensitive information, do not push to github**

# Help and Documentation

## Git/Github Usage

### Setting up

1. Clone this git: `git clone https://github.com/code4ny/NYSecure.git`
1. Change base branch to push/pull from: `git branch -u origin/development`
   - If unsure, just push/pull from here for now.

### Rough Git Workflow

(Assumed that the repository is set up)

1. Select the correct branch.
1. Pull: `git pull`
1. Edit files.
1. Add edited file: `git add <filename>`
1. Commit: `git commit -m '<message>'`
1. Push: `git push`
1. Go github to merge branch if needed.

p.s. If you are using vscode, there is a source control tab that you can use to do step 4-5. And small refresh icons at the bottom for you to push/pull. The branch name is at the bottom. So you don't need to use the command line. Or download any other git gui at https://git-scm.com/downloads/guis.

### Useful commands list

In the case that the gui doesn't have the function

- Add edited files: `git add <filename>` for some file, or `git add .` for everything in the directory
- Commit: `git commit -m '<message>'`
- Push: to send your edited files to the repo `git push`
- Pull: to update your current files from the repo `git pull`
- Select new branch from github branch: `git branch -u origin/<branch-name>`
- Select new branch: `git checkout <branch-name>`
- Check current branch/see all branch: `git branch` (the one with asterisk is the current branch)
