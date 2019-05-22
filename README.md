# gitlab-global-search

git clone git@github.com:huifenqi/gitlab-global-search.git

cd gitlab-global-search

pip install -r requirements.txt

update .gitlab.cfg(Get private_token from `Personal Access Tokens` in gitlab with `api` scope.)

python search.py -w test

python search.py --help
