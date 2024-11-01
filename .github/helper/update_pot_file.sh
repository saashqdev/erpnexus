#!/bin/bash
set -e
cd ~ || exit

echo "Setting Up Wrench..."

pip install saashq-wrench
wrench -v init saashq-wrench --skip-assets --skip-redis-config-generation --python "$(which python)"
cd ./saashq-wrench || exit

echo "Get ERPNexus..."
wrench get-app --skip-assets erpnexus "${GITHUB_WORKSPACE}"

echo "Generating POT file..."
wrench generate-pot-file --app erpnexus

cd ./apps/erpnexus || exit

echo "Configuring git user..."
git config user.email "developers@erpnexus.org"
git config user.name "saashq-pr-bot"

echo "Setting the correct git remote..."
# Here, the git remote is a local file path by default. Let's change it to the upstream repo.
git remote set-url upstream https://github.com/saashqdev/erpnexus.git

echo "Creating a new branch..."
isodate=$(date -u +"%Y-%m-%d")
branch_name="pot_${BASE_BRANCH}_${isodate}"
git checkout -b "${branch_name}"

echo "Commiting changes..."
git add erpnexus/locale/main.pot
git commit -m "chore: update POT file"

gh auth setup-git
git push -u upstream "${branch_name}"

echo "Creating a PR..."
gh pr create --fill --base "${BASE_BRANCH}" --head "${branch_name}" --reviewer ${PR_REVIEWER} -R saashq/erpnexus
