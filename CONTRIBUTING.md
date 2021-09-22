## How to Contribute

Thanks for deciding to contribute to the project! The following instructions will guide you through getting a development set-up going and also offers some guidelines towards submitting good pull requests.

### Requirements

Please make sure you have the following tools installed and correctly set up before proceeding:

- [Python 3.9](https://www.python.org/downloads/)
- [Git for Windows](https://gitforwindows.org/)
- [Make for Windows](https://stackoverflow.com/questions/32127524/how-to-install-and-use-make-in-windows)

As an alternative to the above, you might also be able to use [WSL](https://docs.microsoft.com/en-us/windows/wsl/install). That would spare you the need of having to install tools like `git` and `make` manually, and Python should also be much easier to install and manage via tools like [pyenv](https://github.com/pyenv/pyenv). You can read more about using Python under WSL [here](https://docs.microsoft.com/de-de/windows/python/web-frameworks)

- [poetry](https://python-poetry.org/docs/#osx--linux--bashonwindows-install-instructions) (via bash, i.e. either through Git Bash or WSL if you set that up)


### Setting up the project

Let's start by cloning the project. From a Git Bash session, run:

```shell
git clone github.com https://github.com/pyviator/msfs-geoshot.git
cd msfs-geoshot
```

Next, set up a new python virtual environment and install all dependencies via:

```shell
make install
```

You should now be able to run from source with:

```bash
make run
```


### Submitting changes

1. [Fork the project](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

2. Set up a separate branch and give it a clear name of what you are working on:

    ```
    git checkout -b my-awesome-new-feature
    ```

3. Commit your changes using clear and concise commit messages.

4. Make sure your changes pass the project's checks:

    ```
    make check
    ```

5. Finally, submit your changes as PR, choosing a descriptive title and text.