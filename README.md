<div align='center'>
  
## A React Native app demo for Multi-objective Evolutionary Neural Architecture Search
  
</div>

### Authors:
1. [Tan Ngoc Pham](https://github.com/ngctnnnn/)
2. [Twel Vu](https://github.com/twelcone)
3. [An Vo](https://github.com/vokhanhan25)

---
### Table of contents
#### 1. [Introduction](#1-introduction)
#### 2. [Our contribution](#2-our-contribution)
#### 3. [Implementation details](#3-implementation-details)
#### 4. [Results](#4-results)
#### 5. [Demo](#5-demo)
#### 6. [References](#6-references)

---
### 1. Introduction
#### Automated Machine Learning (AutoML)
- AutoML aims to enable developers with very little experience in ML, to make use of ML models and techniques.
- It tries to automate the end-to-end process of ML in order to proceed simple solutions and create those solutions faster.
- Sometimes, discovered models even outperform fine-tuned models.
- AutoML consists of almost every aspect in making a machine learning pipeline, from drawing dataset to deploying final models.
#### Neural Architecture Search (NAS)
- NAS is a subset of AutoML in which pays much attention to automatically design powerful neural architectures (with one or more constraints, e.g., performance, latency) towards a certain problem formulation.
- Motivation:
  -  Human-design architectures are time-consuming and require specified knowledge from experts.
  -  Achieve superior performance on various tasks.
  -  Higher performance often means higher complexity.
### 2. Our contribution
- In this work, we utilise multi-objective evolutionary algorithm (MOEA) to solve NAS problem as a multi-objective problem to accomplish an optimal front trade-off between performance and complexity.
- We also work out the bottleneck issue in the architectures' performance estimation phase with two objectives:
  - Validation accuracy at epoch 12
  - The floating point operations per second (FLOPs).
### 3. Implementation details
- The experiment conducted in 21 runs.
- NSGA-II is applied with the population size of 20, the number of generations of 50, two points crossover, tournament selection, polynomial mutation.
- We perform our algorithm on multi-objectives which are minimizing valid accuracy at epoch 12/epoch 200 and FLOPs.
- Inverted Generational Distance (IGD) is served as the metric to measure the performance of our MOEA algorithm.
### 4. Results
<div align='center'>
<img width="551" alt="Screen Shot 2022-05-31 at 17 20 24" src="https://user-images.githubusercontent.com/67086934/171151907-378bb182-9468-4b2a-95c6-545f34ba90e9.png"> <p align='center'> <b>Results on CIFAR-10</b> </p> </div>

<div align='center'>
<img width="555" alt="Screen Shot 2022-05-31 at 17 21 54" src="https://user-images.githubusercontent.com/67086934/171152184-f2d7e79b-0d89-47bc-af4b-ebc62fd0ec6d.png"> <p align='center'> <b>Results on CIFAR-100</b> </p> </div>

<div align='center'>
<img width="562" alt="Screen Shot 2022-05-31 at 17 22 03" src="https://user-images.githubusercontent.com/67086934/171152206-56e0cba8-c26f-45b7-a1f6-5db1c2f01a94.png"> <p align='center'> <b>Results on CIFAR-100</b> </p> </div>

<div align='center'>

<img width="548" alt="Screen Shot 2022-05-31 at 17 22 45" src="https://user-images.githubusercontent.com/67086934/171152367-2f2b40f5-9017-47ef-b4fa-eee591f2bd09.png"> <p align='center'> <b>Last archive</b> </p> </div>

<div align='center'>
<img width="748" alt="Screen Shot 2022-05-31 at 17 23 50" src="https://user-images.githubusercontent.com/67086934/171152550-0658d0e0-4e07-4d92-ac73-aec8f4e9a600.png"></div>


<div align='center'>

<img width="591" alt="Screen Shot 2022-05-31 at 17 23 23" src="https://user-images.githubusercontent.com/67086934/171152482-7c4aa376-7240-4e6a-8772-515991b78bb5.png"> </div>

### 5. Conclusions
- Experimentally, using early stopping helps to have an acceptable IGD.
- In terms of accuracy, using valid accuracy at epoch 12 instead of epoch 200 gives similar results. Validating at epoch 12 has an even higher accuracy on CIFAR-10.
- Multi-objectives including performance and complexities enable us to find the trade-off front with miscellaneous architectures.
- Early stopping reduces significantly computational cost, and hence would let NAS be able to apply on diverse datasets. 

### 6. Demo
#### Product design method
- To build a simple yet effective mobile application, we use MVC model:

<div align='center'>

<img width="368" alt="Screen Shot 2022-05-31 at 17 25 37" src="https://user-images.githubusercontent.com/67086934/171152887-56f6db3e-9000-4672-9a95-2cdea50d5d82.png"> </div>

- Our application takes an image containing the object to-be-classified as the input and returns the class of object after being classified with its probability.

#### View
- View is constructed using Javascript-based React Native  
- React Native is a JavaScript framework for writing real, natively rendering mobile applications for iOS and Android. 
- It’s based on React, Facebook’s JavaScript library for building user interfaces, but instead of targeting the browser as it is first introduced, it targets mobile platforms.

#### Controller 
- The controller for the application is built beneath PyTorch framework to realize our aforementioned contribution to the work.

#### Model
- To make a connection between View and Controller and serve as the middle component for the final application, we use Flask - a micro Python-based web framework due to it flexibility, lightweight, and beginner-friendliness.

### 7. References
[1] Elsken, T., Metzen, J. H., & Hutter, F. (2019). Neural architecture search: A survey. The <i>Journal of Machine Learning Research</i>, 20(1), 1997-2017.

[2] Deb, K., Pratap, A., Agarwal, S., & Meyarivan, T. A. M. T. (2002). A fast and elitist multiobjective genetic algorithm: NSGA-II. <i>IEEE transactions on evolutionary computation </i>, 6(2), 182-197.      

[3] Zoph, B., & Le, Q. V. (2016). Neural architecture search with reinforcement learning. <i>arXiv preprint arXiv:1611.01578</i>.    

[4] Real, E., Aggarwal, A., Huang, Y., & Le, Q. V. (2019, July). Regularized evolution for image classifier architecture search. In <i>Proceedings of the AAAI conference on artificial intelligence </i> (Vol. 33, No. 01, pp. 4780-4789).     

[5] Dong, X., Liu, L., Musial, K., & Gabrys, B. (2021). Nats-bench: Benchmarking nas algorithms for architecture topology and size. <i>IEEE transactions on pattern analysis and machine intelligence.</i>      

[6] Coello, C. A. C., & Sierra, M. R. (2004, April). A study of the parallelization of a coevolutionary multi-objective evolutionary algorithm. In <i>Mexican international conference on artificial intelligence</i> (pp. 688-697). Springer, Berlin, Heidelberg.

