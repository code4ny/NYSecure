# Project

## Project Structure

- Codes to be in the folder named `app`.
- Main flask code is in `app/views.py`.
- To run the flask code, run the `run.py` file.
- Create any other files needed to improve the structure.

## Project Specifications (for MVP)

- All form datas should be using POST unless there is a specific purpose for using GET.

### Reporting page

- Should obtain the information:
    + name
    + location
    + is the room secure against intrusion?

### Summary page

- Shows the number of people at each block. 
- When clicked, get data, and show locations at the block and the number of people.

## Job Scope

### Backend

- Come up with a database schema
- Able to update the database based on data from location_reporting
- Appropriate data structure/object to be passed to render template

### Frontend

- Design the page and beautify it.
- Coding the html to display all datas (including the jinja expressions)

## Heroku

- Go to `http://nysecure.herokuapp.com/` to view the app
- Maintenance mode to be on by default.

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

p.s. If you are using vscode, there is a source control tab that you can use to do step 4-5. And small refresh icons at the bottom for you to push/pull. The branch name is at the bottom. So you don't need to use the command line. Or download any other git gui.

### Useful commands list

In the case that the gui doesn't have the function

- Add edited files: `git add <filename>` for some file, or `git add .` for everything in the directory
- Commit: `git commit -m '<message>'`
- Push: to send your edited files to the repo `git push`
- Pull: to update your current files from the repo `git pull`
- Select new branch from github branch: `git branch -u origin/<branch-name>`
- Select new branch: `git checkout <branch-name>`
- Check current branch/see all branch: `git branch` (the one with asterisk is the current branch)
