var express = require('express');
var fileUpload = require('express-fileupload');
var uuid = require('uuid');
var spawn = require('child_process').spawn;

var app = express();

app.use(express.static('client/', {
  'extensions': ['html']
}));

app.use(express.static('results/'));

app.use(fileUpload());

function invokePythonScript(params, callback) {

//  var command = spawn('cp', [
//    params.inputPath,
//    outputPath
//  ]);

   var command = spawn('python', params);

   console.log(params[params.length - 1]);

  command.on('close', function (code) {
    if (code === 0) {
      callback({
        success: true,
        outputPath: params[params.length - 1]
      });
    }
    else {
      console.log(code)
      callback({
        success: false,
        outputPath: params.inputPath
      });
    }
  });
}

app.post('/detectRectangles', function (req, res) {
  if (!req.files || !req.files.image) {
    res.sendStatus(422);
  }
  else {
    var uploadPath = process.cwd() + '/uploads/' + uuid() + '.jpg';
    var imageFile = req.files.image;
    imageFile.mv(uploadPath, function (err) {
      if (err) {
        res.status(500).send(err);
      }
      else {
        var scriptParams = {
          scriptPath: "rectangleDetection.py",
          inputPath: uploadPath,
          colorR: req.body.colorR,
          colorG: req.body.colorG,
          colorB: req.body.colorB,
          colorPercentage: req.body.colorPercentage,
          faultTolerance: req.body.faultTolerance
        };

        var outputPath = process.cwd() + '/results/' + uuid() + '.jpg';

        invokePythonScript([
           scriptParams.scriptPath,
           scriptParams.inputPath,
           scriptParams.colorR,
           scriptParams.colorG,
           scriptParams.colorB,
           scriptParams.colorPercentage,
           scriptParams.faultTolerance,
           outputPath
         ], function (result) {
          if (result.success) {
            res.sendFile(result.outputPath);
          }
          else {
            res.sendStatus(500);
          }
        });
      }
    });
  }
});

app.post('/processImage', function (req, res) {
  if (!req.files || !req.files.image) {
    res.sendStatus(422);
  }
  else {
    var uploadPath = process.cwd() + '/uploads/' + uuid() + '.jpg';
    var imageFile = req.files.image;
    imageFile.mv(uploadPath, function (err) {
      if (err) {
        res.status(500).send(err);
      }
      else {
        var outputPath1 = process.cwd() + '/results/' + uuid() + '.jpg';

        var scriptParams = {
          scriptPath: 'brightnessAndContrast.py',
          inputPath: uploadPath,
          brightness: req.body.brightness,
          contrast: req.body.contrast,
          result1Path: outputPath1
        };

        invokePythonScript(
          [scriptParams.scriptPath, scriptParams.inputPath, scriptParams.brightness, scriptParams.contrast, scriptParams.result1Path], 
          function (result) {
          if (result.success) {
            res.sendFile(result.outputPath);
          } else {
            res.sendStatus(500);
          }
        });
      }
    });
  }
});

app.post('/drawContours', function (req, res) {
  if (!req.files || !req.files.image) {
    res.sendStatus(422);
  }
  else {
    var uploadPath = process.cwd() + '/uploads/' + uuid() + '.jpg';
    var imageFile = req.files.image;
    imageFile.mv(uploadPath, function (err) {
      if (err) {
        res.status(500).send(err);
      }
      else {
        var outputPath = process.cwd() + '/results/' + uuid() + '.jpg';

        var scriptParams = {
          scriptPath: 'drawContours.py',
          inputPath: uploadPath,
          result2Path: outputPath
        };

        invokePythonScript(
          [scriptParams.scriptPath, scriptParams.inputPath, outputPath], 
          function (result) {
          if (result.success) {
            res.sendFile(result.outputPath);
          } else {
            res.sendStatus(500);
          }
        });
      }
    });
  }
});



app.listen(3000);

