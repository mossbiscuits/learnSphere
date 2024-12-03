# LearnSphere

This is a final project for CS5060 at Utah State University.

## Bayesian Methods

Handle dependencies by running the following commands:

```
python3 -m venv .lsvenv
source .lsvenv/bin/activate
pip3 install numpy matplotlib scipy
```

Run the algorithms with the following commands:

- Content type selection: `python3 bayesian/content.py`
- Learning pathway selection: `python3 bayesian/pathways.py`
- Quiz customization: `python3 bayesian/quizzes.py`
  - See old versions of quiz customization with lower scores at `bayesian/quizzes/quizzes#.py`

See the pre-generated (on our machines) results at:
- Content type selection: `bayesian/content/results.txt` and the plots contained in that folder
- Learning pathway selection: `bayesian/pathways/results.txt` and the plots contained in that folder
- Quiz customization: `bayesian/quizzes/results.txt` 
  - See old versions of quiz customization with lower scores at `bayesian/quizzes/results#.txt`

## Explore / Exploit

Run the algorithm and view a plot with the following command:
```
python3 exploreExploit/finalProject.py
```

Further documentation is found at https://github.com/mossbiscuits/learnSphere/blob/main/exploreExploit/README.md
