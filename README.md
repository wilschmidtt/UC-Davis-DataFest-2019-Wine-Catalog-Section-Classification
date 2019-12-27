# UC Davis DataFest 2019 - Section Detector
#### The Challenge 
The UC Davis Library has over 200 scanned catalogs spanning nearly a 50 year period. How do we translate a scanned image
into usable data for economists, historians, archivists, and other researchers?
#### Hypothesized Solution
Unstructured text recognition using Python and Spyder. Utilize Pandas, NumPy, Matplotlib, and sklearn. Clustering 
by feature location was done with K-Means machine learning algorithm.

[DataFest Website](http://ds.lib.ucdavis.edu/eventscalendar/datafest-wine-catalog-challenge/)

## Libraries to Install
* psycopg2 - DB API 2.0 compliant PostgreSQL driver
  - `conda install -c anaconda psycopg2`
* matplotlib - plotting library for NumPy
  - `conda install -c conda-forge matplotlib`
* pandas - software library for data manipulation and analysis
  - `conda install -c anaconda pandas`
* scikit learn - machine learning library
  = `conda install -c anaconda scikit-learn`
* numpy - general-purpose array-processing package
  - `conda install -c anaconda numpy`

### Prerequisites
* Anaconda (Python 3.7 Version)
  - [Anaconda Instillation Instructions](https://docs.anaconda.com/anaconda/install/)
* UC Davis VPN (optional - used for viewing the wine catalouges)
  - VPN can only be installed if you are a UC Davis student/staff
  - [VPN - Instillation and Use Instructions](https://www.library.ucdavis.edu/service/connect-from-off-campus/)

## Running the tests

* Simply open Anaconda, launch Spyder (used version 3.3.6 to create this program, but it shouldn't matter which version you run it on),
  and select all the code and run it at once. 
* In both the terminal and the working directory for this program you will see a series of scatter plots titled, 'Cluster of Words',
  each with a cooresponding iteration.
  - Iteration 0: Scatter plot of all the words that appear on the desired catalog before any manipulation has been done.
  - Iteration 1: Scatter plot of all the words, except this time they are color coded based off of what cluster they fall into (NOTE:
    The elbow method was used to determine the optimal number of clusters for each iteration of the data. An image of the line graph
    used for the elbow method can be seen within the terminal.)
  - Iteration 2: Each of the clusters from iteration 1 are placed within their own dataframe, and these clusters are then broken up into     their respective ideal number of clusters. The result should be a minimum of four new scatter plots.
  - Iteration 3 (optional): If you look at the scatter plots and notice that one can still be broken down nicely into groups of 
    different clusters, then you can enter the name of the cluster in question, and it will be broken down into its constituent sub-
    clusters. A .png for each of the scatter plots created will be saved within the working directory.
    - If desired

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
