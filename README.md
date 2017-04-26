
# Maria Demo
### _Making Automated Rapid Intelligent Assignments_


```python
# Let's import some things that will help us
from utils import repo_utils as repo, time_utils as tutil, string_utils as sutil
```


```python
# Now, let's start a timer, just for fun :)
dr_jin = tutil.new_timer(10)
```

    
    Time Remaining: 10 minutes 0 seconds
    

The goal of this notebook is to provide an interactive tour through some of the ideas behind Maria, and the results that those ideas led to.  

### What was I doing?

* Bugs are among us
* Bugs are ~~not~~ features 
* Bugs need to be fixed
* Let's provide a way to automatically assign bugs to developers who can fix them
* We'll use projects on Github because they're available

### Cool, so how?
* Well, there could be a couple of ways
* _Who should fix this bug?_ -> based on body and title of issue
    * There were some problems
        * Assigned to field not reliable
        * Had to use project specific heuristics instead
        * Didn't port well to GCC
* My approach -> Use exceptions and last code touch
    * _Who should fix this bug?_ stated that only 11% of bug reports in Eclipse had stack traces...
    * So what would this look like?
        ```
        issues_with_filenames <- List
        predictions <- List
        actual <- List
        for issue in issues_with_filenames:
            prediction
            file_names_in_issue = get_file_names_from_issue_body()
                for file_name in files_names_in_issue:
                    if commit_database_has_file_name:
                        prediction = get_last_editor
                        actual.append(issue.closer)
                        break
                    else:
                        continue
            predictions.append(prediction)
        
       compare(actual, predictions)
       ```


```python
print(dr_jin)
```

    
    Time Remaining: 9 minutes 56 seconds
    

### What repositories to study?
* I chose three repositories:
    * Number of Commits
    * Number of Contributors
    * Number of Issues
    * Language


```python
# Let's talk about the repo's that we will be looking at.  
keras = repo.new_repo('keras', 'fchollet', 'python')
spring_boot = repo.new_repo('spring-boot', 'spring-projects', 'java')
tensorflow = repo.new_repo('tensorflow', 'tensorflow', 'c++')
repos = [keras, spring_boot, tensorflow]
[print(r) for r in repos]
print(dr_jin)
```

    Repo: keras           Owner: fchollet        Primary Language: python         
    Repo: spring-boot     Owner: spring-projects Primary Language: java           
    Repo: tensorflow      Owner: tensorflow      Primary Language: c++            
    
    Time Remaining: 9 minutes 52 seconds
    

### Prep
Some work went in ahead of time to gather this data and generate the statistics you'll see below.  As I mentioned in the talk on _Who should fix this bug?_ **data is dirty**.  

Some fixes:
* Sanitize Strings -- Remove single quotes, double quotes, newline, return carriage, remove extra some non-alphabetic characters
* Fill missing values -- Some fields are **not** set, so instead of a null value, had to fill in with something that would process 
    * Ex: Empty string instead of null
* 

#### Commits
I cloned the three above repositories and ran `git log --stat` on each.  That command produced output:
```
commit 7c6463da6f972ffaa466b0f55d06b760a98caf8e
Author: Carl Thomé <carlthome@gmail.com>
Date:   Tue Apr 4 20:28:16 2017 +0200

    Spelling (#6149)

 examples/lstm_benchmark.py | 4 ++--
 1 file changed, 2 insertions(+), 2 deletions(-)

commit 4785d51705949e72316770413ba187f07f05a5bc
Author: Fariz Rahman <farizrahman4u@gmail.com>
Date:   Tue Apr 4 22:03:58 2017 +0530

    Typo fix (#6141)

 keras/engine/topology.py | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
                 .
                 .
                 .
```

I inserted this data into Neo4j, a leading graph database, to capture the relationships between files, commits, and authors.  

#### Issues
Once I had the commits, I had to pull the issues down from Github using a Python library (PyGithub) which interfaced with their API. This only provided 5000 requests per hour, so this stage took a little bit longer.  

The `title`, `body`, `assigned_to`, `closed_by`, and `labels` fields were the stored in an H2 database (one for each repository).  Once this was complete, I could start looking at the what I had to work with...  

### Some Simple Statistics


```python
print('{0:15} {1:10} {2:15} {3:10} {4:12} {5:10}'.format("Repository", "Commits", "Contributors", "Issues", "Exceptions", "Files"))
[print('{0:15} {1:10} {2:15} {3:10} {4:12} {5:10}'.format(r.repository, r.get_number_of_commits(), r.get_number_of_contributors(), r.get_number_of_issues(), r.get_number_of_exceptions(), r.get_number_of_files())) for r in repos]
print(dr_jin)
```

    Repository      Commits    Contributors    Issues     Exceptions   Files     
    keras           3439       446             2126       127          375       
    spring-boot     11456      417             5487       923          11735     
    tensorflow      16097      856             5064       255          16198     
    
    Time Remaining: 9 minutes 33 seconds
    


```python
repo.plot_multiple_lists([r.get_authors_of_commits() for r in repos], [r.repository for r in repos],50)
```




<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~bcpilche/9.embed" height="525px" width="100%"></iframe>



So the number of exceptions vs issues looks kinda bad there... lets look at those percentages


```python
[print('{0:15} {1:10} {2:10}'.format(r.repository, r.get_number_of_exceptions(), r.get_issue_percentage(r.num_of_exceptions))) for r in repos]
print(dr_jin)
```

    keras           127        5.97%     
    spring-boot     923        16.82%    
    tensorflow      255        5.04%     
    
    Time Remaining: 9 minutes 6 seconds
    

Eeeeekkkk... Not looking good for my idea.

In _Who should fix this bug?_ they were able to achieve 57% and 64% accuracy.  Much better than I can do utilizing my method.

What if we look at issues that have a file name in the body of the issue?


```python
[print('{0:15} {1:10} {2:10}'.format(r.repository, r.get_number_issues_with_filenames(), r.get_issue_percentage(r.num_of_issues_with_filenames))) for r in repos]
print(dr_jin)
```

    keras           726        34.15%    
    spring-boot     1253       22.84%    
    tensorflow      2486       49.09%    
    
    Time Remaining: 9 minutes 2 seconds
    

Combining the two we get:


```python
[print('{0:15} {1:10} {2:10}'.format(r.repository, r.get_number_of_issues_with_excep_or_filename(), r.get_issue_percentage(r.num_of_issues_with_excep_or_filename))) for r in repos]
print(dr_jin)
```

    keras           780        36.69%    
    spring-boot     1528       27.85%    
    tensorflow      2562       50.59%    
    
    Time Remaining: 8 minutes 59 seconds
    

So some headway can be made. But this approach, even if 100% accurate, will not provide a lot of help. At least compared to baseline of _Who should fix this bug?_ 

So let's look at all of these issues that have either an exception listed in them or a filename and see who fixed them.


```python
repo.plot_multiple_lists([r.get_closer_data(r.get_excep_or_filename()) for r in repos],[r.repository for r in repos],50)
```




<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~bcpilche/9.embed" height="525px" width="100%"></iframe>



So, the Keras repository would almost be easiest to just predict the top contributor:


```python
repo.get_top_of_list(keras.get_closer_data(keras.get_excep_or_filename()))[0]
```




    ''



### Just for kicks and giggles, let's try it anyways...


```python
# Gotta import it:
from runner import last_touch
for r in repos:
    last_touch.run(r)
print(dr_jin)
```

    
    Time Remaining: 1 minutes 47 seconds
    


```python
print('{0:15} {1:10} {2:21} {3:15} {4:15} {5:20} {6:10}'.format("Repository", "Issues", "Exception/FileName", "File in Repo", "Unpredictable", "Predicted Correctly", "Percentage"))
[r.print_results() for r in repos]
print(dr_jin)
```

    Repository      Issues     Exception/FileName    File in Repo    Unpredictable   Predicted Correctly  Percentage
    keras           2126       780                   518             107             58                   14.11%    
    spring-boot     5487       1528                  556             216             143                  42.06%    
    tensorflow      5064       2562                  1802            940             49                   5.68%     
    
    Time Remaining: 1 minutes 47 seconds
    

## Final Thoughts

### Data can never be too clean, always ensure you strip unwanted characters

### Make sure your data lines up
* Commit history -> (Name, email)
* Issues on Github -> (Name (maybe), email (maybe), login)

### Issues don't typically include filenames or exceptions


```python
[print('{0:15} {1:10} {2:10}'.format(r.repository, r.get_number_of_issues_with_excep_or_filename(), r.get_issue_percentage(r.num_of_issues_with_excep_or_filename))) for r in repos]
print(dr_jin)
```

## Extra things:











#### What are some things that one of the developers worked on?


```python
fchollet = []
for tup in keras.results:
    if "francois.chollet@gmail.com" in tup[0]:
        fchollet.append(tup[0][0])
fchollet[:10]
```




    ['TypeError running keras example',
     'LSTM with different length of sequences',
     'Error running imdb example',
     'K.batch_dot() doc example fails w/ Tensorflow backend',
     'Embedding layer w/ mask in a nested model',
     'Unused function in generic_utils.py',
     'Wrong source links for merge layers',
     'in_top_k() gives different results for Theano and TensorFlow backends',
     'AttributeError: module object has no attribute convolution in cifar10_cnn.py',
     'Calling call method of Layer class in topology.py with wrong parameters']



#### What were some of the correct predictions?


```python
keras.predicted_correctly[:10]
```




    [('Error running imdb example',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('IndexError: index 1 is out of bounds for axis 1 with size 1',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('TypeError: moments() got an unexpected keyword argument shift',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('Travis-CI failing due to truncated Pickle',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('Wrong weights Initialization in tf mode',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('An error occured when run babi_memnn.py in theano backend, but in tensorflow backend its ok',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('Imagenet_utils - Incorrect input shape error check',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('Pre-trained nets crash with theano ordering',
      'Francois Chollet',
      'francois.chollet@gmail.com'),
     ('RMSProp looks wrong', 'Francois Chollet', 'francois.chollet@gmail.com'),
     ('Fine-tuning pre-trained VGG16 not possible since `add` method is not defined for `Model` class?',
      'Francois Chollet',
      'francois.chollet@gmail.com')]



#### Did the predictions follow the original distribution?


```python
all_preds = []
for r in repos:
    pred_author = []
    for a in r.results:
        if a[1] in r.predicted_correctly:
            pred_author.append(a[0][1])
    all_preds.append(pred_author)
repo.plot_multiple_lists(all_preds,[r.repository for r in repos],50)
```




<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plot.ly/~bcpilche/9.embed" height="525px" width="100%"></iframe>



So _Who should fix this bug?_ limited the developers they included in their study by developer activity.  It appears as though this method may not get you around that issue.
