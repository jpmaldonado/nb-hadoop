REGISTER 'naive_bayes.py' USING jython AS NBClassifier;


traffic = LOAD 'yourschema.yourtable' USING org.apache.hive.hcatalog.pig.HCatLoader();


classified = FOREACH traffic GENERATE NBClassifier.predict(resource);

DUMP classified;

--STORE classified into 'classified.txt';
