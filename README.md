##Maria: Making Automated Rapid Intelligent Assignments
The goal of this project is to reduce the time it takes to assign a bug or issue to the right person.  By using
code touch and comment history, Maria will be able to provide a number of good suggestions for watchers and assignees.

###Current Status
This project currently only reads a manually generated git log file (git log --stat) and creates a Neo4j database from
it.