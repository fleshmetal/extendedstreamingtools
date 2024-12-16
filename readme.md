# Assignment 2 - README

**Student:** Anthony Romy Paul | apaul63
[OverLeaf READONLY link](https://www.overleaf.com/read/mqftdxrwmfmr#ed17c4)

## Intro

This is my submission A2 for Fall 2024 ML. I copy and pasted this structure from my A1 submission.

## Repo Contents 

There are 2 main folders with the major files.
1. **notebooks**: A folder containing three notebooks, where all study is performed. Each notebook is for a specific problem. Additionally, multiple images are present, which were generated from code.
2. **data**: A folder containing the dataset used for the NN weight updating 

There is 1 extra file other than this README:
1. A requirements.txt file for setting up the environment

## Retrieving and Running Code

> _Generative AI Note:_ Multiple sections of code were written, modified, and tuned by ChatGPT Auto. Occasionally, I would see that I would be getting ChatGPT-4o results until the timer for usage expired. I do not pay for the plus account. Additionally, I would often have an idea, make a base code template, and then ask ChatGPT to add or compress features in a format that would enable the diagrams to look the way they do in my paper. I also used resources and code from the [mlrose-ky library](https://nkapila6.github.io/mlrose-ky/). This included methods to use and index through the runner results. This was my first time using a runner to generate multiple tests.  

My code is two Jupyter notebooks within the **playground** directory.

- fourpeaks_nb.ipynb
- neural_nn.ipynb

Each section is broken out and organized, and both follow the exact same structure:

1. Importing data
2. Grid search tuning at end points (10, 100) for hyperparameter selections.
3. Final model testing


### Retrieving the libraries: 

An additional requirements.txt file is provided to detail how my environment needs to be set up to run these notebooks. Please use this command:

```bash
pip install -r requirements.txt
```

Once all the requirements are installed, you can run all the notebook cells with the 'Run All' command in your IDE. There is no spaghetti logic, so no runtime error should arise. However, some of the runtimes are insane. Proceed with caution when running! 

## Retrieving and Reading Data

The datasets were downloaded from Kaggle. They are provided in the repo in the **data** folder and import is handled in code.

**You WILL need to change the input parameter for the directory link to your own!!** 
```bash
train_df = pd.read_csv('/Users/anthony/Documents/Masters/ML/A2/data/titanic_kaggle/train.csv')
```

But for you, the Instructors/TAs, it should be modified to look something like this:

```bash
train_df = pd.read_csv('/TheLocationWhereThisFileIsOnYourComputer/data/titanic_kaggle/train.csv')`
```

The original datasets can be found here:
1. [Titanic - Machine Learning from Disaster](https://www.kaggle.com/c/titanic)
