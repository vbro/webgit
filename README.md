# WebGit

**WebGit** is a command line program written in Python, that allows the user to open commonly used GitHub/GitLab pages.

### Usage examples
The following examples are from a directory cloned from [Kafka](https://github.com/apache/kafka).

* ```webgit```  
Opens https://github.com/apache/kafka
  

* ```webgit #4501``` or ```webgit 4501```  
Opens https://github.com/apache/kafka/pull/4501
  

* ```webgit 642da2f28c9bc6e373603d6d9119ce33684090f5```  
Opens https://github.com/apache/kafka/commit/642da2f28c9bc6e373603d6d9119ce33684090f5
  

* ```webgit 642da2f```  
Opens https://github.com/apache/kafka/commit/642da2f
  

* ```webgit 642da2f README.md```  
Opens https://github.com/apache/kafka/blob/642da2f/README.md
  

* ```webgit tree 2.8.1-rc1```  
Opens https://github.com/apache/kafka/tree/2.8.1-rc1
  

* ```webgit tree 2.8.1-rc1 config/zookeeper.properties```  
Opens https://github.com/apache/kafka/blob/2.8.1-rc1/config/zookeeper.properties
  

* ```webgit prs```  
Opens https://github.com/apache/kafka/pulls
  

* ```webgit myprs```  
Opens https://github.com/apache/kafka/pulls?q=is%3Apr+author%3Avbro
  

* ```webgit issues```  
Opens https://github.com/apache/kafka/issues
  

* ```webgit issues 370```  
Opens https://github.com/apache/kafka/issues/370


### Installation

1. Verify that [Python 3](https://www.python.org/downloads/) is installed

2. Clone the repository
    ```bash
    git clone https://github.com/vbro/webgit
    ```

3. Make sure that webgit.py is executable, for example
    ```bash
    chmod +x webgit/webgit.py
    ```

4. Create a symlink for **WebGit** in a directory in `$PATH`, for example
    ```bash
    ln -s webgit/webgit.py /usr/local/bin/webgit
    ```


### Help text
```pre
% webgit --help
usage: webgit [-h] [-a] [-C PATH] [-f FILE] [-o ORG] [-u GIT_USER] [-r REMOTE] [command [command ...]]

Open Github and Gitlab web pages

positional arguments:
  command               commits - open webpage for commits
                        repo    - open webpage for repo (default behavior)
                        org     - open webpage for organization
                        user    - open webpage for user
                        pr      - open webpage to create a pull request page
                        prs     - open webpage for all pull requests
                        myprs [username]    - open webpage for pull requests for specified user
                        issue [number]      - open webpage for specified issue
                        issues   - open webpage for all issue
                        tree [commit | branch | tag] - open webpage for commit, branch or tag tree
                        [commit_hash] (e.g 76ac43b)  - open webpage for commit
                        [pull_request_number] (e.g. 7, 3034, #1234567) - open webpage for pull request

optional arguments:
  -h, --help            show this help message and exit
  -a, --print-address   print the web address
  -C PATH, --path PATH  git repository directory
  -f FILE, --file FILE  full repository path for file or directory
  -o ORG, --org ORG     git web org or project name
  -u GIT_USER, --git-user GIT_USER
                        git web username, e.g. username for github
  -r REMOTE, --remote REMOTE
                        the git remote to use, e.g. main, upstream
```


### Contributing
Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md). 


### License
**WebGit** uses the [MIT License](LICENSE)
