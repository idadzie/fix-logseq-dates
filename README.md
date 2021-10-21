# Fix Logseq dates

This is a CLI tool to fix the date references following a change in date format since the current version (0.4.4) of [Logseq](https://logseq.com) does not support this yet.

I built this because I had a similar issue as reported on the Logseq forum and Discord.

 * [Adjusting your preferred date format should also adjust pre-existing date-page references](https://discuss.logseq.com/t/adjusting-your-preferred-date-format-should-also-adjust-pre-existing-date-page-references/2616)

 * [Message One](https://discord.com/channels/725182569297215569/725182570131751005/892017691949404220)

 * [Message Two](https://discord.com/channels/725182569297215569/735747000649252894/895529918786584616)



## :package: Dependencies

It requires [Python](https://www.python.org) **3.6+** to run.



## :floppy_disk: Installation

Install using [pipx](https://pypa.github.io/pipx) if you have it already. Otherwise you can use pip.

#### Via pipx (Recommended)

```shell
 pipx install git+https://github.com/idadzie/fix-logseq-dates
```

#### Via pip

```shell
 pip install git+https://github.com/idadzie/fix-logseq-dates
```



## :rocket: How to use

```
usage: fix-logseq-dates [-h] [-f FORMAT] [-j JOURNALS_DIRECTORY]
                        [-p PAGES_DIRECTORY] [-d GRAPH_DIRECTORY] [--any-date]

CLI tool to fix linked references for Logseq dates.

optional arguments:
  -h, --help             show this help message and exit
  -f FORMAT              date format. (default: MMMM DD, YYYY)
  -j JOURNALS_DIRECTORY  journals folder name. (default: journals)
  -p PAGES_DIRECTORY     pages folder name. (default: pages)
  -d GRAPH_DIRECTORY     absolute path to your local Logseq graph. (default: None)
  --any-date             match any date found not only referenced ones. (default: False)
```



 1. Backup your Logseq graph (directory/folder that contains your markdown files). A simple copy to another directory is enough. :smile:

 2. Run the `fix-logseq-dates` command against your Logseq graph. See [**here**](https://arrow.readthedocs.io/en/latest/#supported-tokens) for supported date format tokens.

    ```shell
    # Example
    fix-logseq-dates -f 'MMMM DD, YYYY' -d ~/path/to/knowledge-graph

    # If you've modified the Journals and/or Pages directories.
    fix-logseq-dates -f 'MMMM DD, YYYY' -d ~/path/to/knowledge-graph -j alt_journals -p alt_pages

    # Match any date strings in the files.
    # Use with caution. It might modifiy unintended dates.
    fix-logseq-dates -f 'MMMM DD, YYYY' -d ~/path/to/knowledge-graph -j alt_journals -p alt_pages --any-date
    ```

3. Open Logseq and re-index your graph.



## :bulb: Tip

If you are familiar with [git](https://git-scm.com) and have some time to spare, you could initialize your Logseq graph as a git repository before running the fix. Then, after the fix, you could use a visual diff tool like [meld](https://meldmerge.org/) to verify your data was modified correctly.



## :sparkling_heart: Like this project ?

Leave a :star: If you think this project is cool.



