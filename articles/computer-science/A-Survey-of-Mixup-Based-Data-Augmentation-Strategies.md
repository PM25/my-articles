## Introduction

Machine learning and deep learning show huge impacts on many different areas in the past decades. They both are data-driven approaches, which means they need a bunch of data to make it work or even to get better performance. But in reality, some data are very expensive or very hard to acquire. For example, fraud detection, where fraud samples are much difficult to obtain than the normal data. Medical images require doctors or people with medical expertise to label, which are very expensive and time-consuming. Insufficient data hurt the performance of deep learning and machine learning, which makes it a critical issue to be solved. There are many ongoing types of research trying to tackle this problem, like one-shot learning, active learning, transfer learning, and many others more. These are just the tips of the iceberg. Data augmentation is also one of them. Many data augmentation strategies are quite naive and simple but yet researches show they give a robust improvement in many different tasks. Mixup is one of the data augmentation strategies that shed the light on in recent years, which also inspire many following works to come out. In this article, I will give a quick introduction to different mixup-based data augmentation strategies.

## What is data augmentation?

Data augmentation is a technique that generates new data from the original training data. Training models with newly generated data can have beneficial effects, like improve performance, increase robustness, and balanced the data. It can be very helpful when the data are insufficient or imbalanced. Even applied it to regular data can help us gain a performance boost.

Some of the simplest forms of data augmentation are rotation, crop, blur, or applying other effects to the original image, illustrated in the figure below. The newly generated images have the same label as the original image.

<figure>
    <img 
    src="https://imgur.com/GXzRum7.png"
    alt="Different Data Augmentation Techniques">
    <figcaption align = "center"> 
    Source: https://arxiv.org/pdf/2002.05709.pdf
    </figcaption>
</figure>

Synthetic Minority Oversampling TEchnique, or SMOTE for short is a very classic data augmentation approach in the early days. It was designed to tackle imbalanced data for traditional machine learning models. SMOTE creates new data by selecting a minority class sample then mixing it with its k nearest same class samples. Using SMOTE can create as much new data as possible. It is simple and effective.

## What is Mixup?

Ongoing...

## Mixup-based strategies

Here are the quick survey of each mixup-based data augmentation strategies.

### Mixup

Ongoing...

arxiv: https://arxiv.org/abs/1710.09412
github: https://github.com/facebookresearch/mixup-cifar10

### CutMix

Ongoing...

arxiv: https://arxiv.org/abs/1905.04899
github: https://github.com/clovaai/CutMix-PyTorch

### Manifold Mixup

Ongoing...

arxiv: https://arxiv.org/abs/1806.05236
github: https://github.com/vikasverma1077/manifold_mixup

### PatchUp

Ongoing...

### SaliencyMix

Ongoing...

### PuzzleMix

Ongoing...

### SmoothMix

Ongoing...

### Co-Mixup

Ongoing...

### FMix

Ongoing...

## Conclusion

Thanks for reading. I'm still an ongoing learner of deep learning and English writing. If you spot on any mistake or have any suggestions are highly appreciated!
