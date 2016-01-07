var express = require('express');  
var path = require('path');  
var app = express();  
var router = express.Router();

app.set('views', path.join(__dirname, 'views'));  
app.set('view engine', 'jade');

app.use(router);  
app.use(express.static(path.join(__dirname, 'public')));

prototype.use(express.static('public'));

router.all('/', function (req, res, next) {  
  console.log('Someone made a request!');
  next();
});

router.get('/', function (req, res) {  
  res.render('index');
});

module.exports = app;