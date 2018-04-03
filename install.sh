#!/bin/bash
shopt -s globstar

# --------------------------------------------------------
# DEFINE LOCAL VARIABLES
# ========================================================
NORMAL=$(tput sgr0)
GREEN=$(tput setaf 2; tput bold)
YELLOW='\033[1;33m'
RED=$(tput setaf 1; tput bold)
NC='\033[0m' # No Color


# --------------------------------------------------------
# COMMON FUNCTIONS
# ========================================================
command_exists () {
  type "$1" &> /dev/null ;
}

command_not_exists () {
  ! type "$1" &> /dev/null ;
}

function red() {
  echo -e "$RED$*$NORMAL"
}

function green() {
  echo -e "$GREEN$*$NORMAL"
}

function yellow() {
  echo -e "$YELLOW$*$NORMAL"
}

function message() {
  printf "%0.s$1-" {1..80}.; printf "\n"
  echo $2
  printf "%0.s=" {1..80}; printf "\n"
  printf "${NC}"
}

# --------------------------------------------------------
# BEGIN INSTALLATION OF DEPENDENCIES
# ========================================================
if [ ! -f .install ]; then
  message $YELLOW "Let's check  npm and npx are installed"

  # install pre commit hooks
  mkdir -p .git/hooks
  cp .git-hooks/* .git/hooks/

  echo `date` >> .install
else
  message $GREEN "Your system Linux dependencies have been installed already"
fi


# update ctags for the project
if command_exists ctags ; then
    ctags -e -R apps/ libs/ ui/**/js/**/*.js templates TAGS
fi

# final message
type cowsay &> /dev/null && cowsay "Let's go installing npm dependencies!" ||
    message $GREEN "Let's go installing npm dependencies!"
printf "\n"
