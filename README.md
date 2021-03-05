# Help and Documentation

## Git/Github Usage

### Setting up

1. Clone this git: `git clone https://github.com/code4ny/NYSecure.git`
1. Change base branch to push/pull from: `git branch -u origin/development`
    - If unsure, just push/pull from here for now.


### Rough Git Workflow

(Assumed that the repository is set up)

1. Select correct branch.
1. Pull: `git pull`
1. Edit files.
1. Add edited file: `git add <filename>`
1. Commit: `git commit -m '<message>'`
1. Push: `git push`
1. Go github to merge branch if needed.

p.s. If you are using vscode, there is a source control tab that you can use to do step 4-5. And small refresh icons at the bottom for you to push/pull. The branch name at the bottom. So you don't need to use command line. 

### Useful commands list

In the case that the gui doesn't have the function

- Add edited files: `git add <filename>` for some file, or `git add .` for everything in the directory
- Commit: `git commit -m '<message>'`
- Push: to send your edited files to the repo `git push`
- Pull: to update your current files from the repo `git pull`
- Select new branch from github branch: `git branch -u origin/<branch-name>`
- Select new branch: `git checkout <branch-name>`
- Check current branch/see all branch: `git branch` (the one with asterisk is the current branch)

## Project Structure

- Codes to be in folder named app.
- Main flask code is in `app/views.py`
- To run the flask code, run the run.py file.