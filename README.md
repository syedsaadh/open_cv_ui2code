# open_cv_ui2code

## Steps To Detect Component
1. Install and setup tensorflow [https://www.tensorflow.org/install/]
2. Activate Tensorflow Environment
3. Install following packages
 - imutils
 - numpy
 - opencv-python
 - matplotlib
 - pandas
 - pillow

To install 
<br> `pip install pandas`

4. Set Environment Variables<br>
```IMAGE_SIZE=224``` <br>
```ARCHITECTURE="mobilenet_0.50_${IMAGE_SIZE}"```

5. To Train <br>
``python -m scripts.retrain \
  --bottleneck_dir=tf_files/bottlenecks \
  --how_many_training_steps=500 \
  --model_dir=tf_files/models/ \
  --summaries_dir=tf_files/training_summaries/"${ARCHITECTURE}" \
  --output_graph=tf_files/retrained_graph.pb \
  --output_labels=tf_files/retrained_labels.txt \
  --architecture="${ARCHITECTURE}" \
  --image_dir=images/
  ``
6. To Predict Component

``` python detect_component.py --image=predict/web.png ```

### To Render on Webpage

1. cd to `myapp`
2. `npm install`
3. `npm start`
4. Now detect components for a image and it will automatically reflect on Webpage